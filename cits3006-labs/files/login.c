/*
 * login.c — a password checker, used the normal way.
 *
 * The SECRET lives only in this program. Whoever runs it can send a guess and
 * learn one bit — "granted" or "denied" — and (unavoidably) observe how long the
 * check took. The attacker (attack.c) is a SEPARATE program: it never sees this
 * secret; it can only talk to this one through its stdin/stdout and time it.
 *
 * Build it TWO ways (the Makefile does both):
 *     cc -O2 -o login                  login.c     VULNERABLE (early-return compare)
 *     cc -O2 -DCONSTANT_TIME -o login_safe login.c FIXED      (constant-time compare)
 *
 * Use it TWO ways:
 *     ./login <password>    check once; prints a verdict; exit 0=granted 1=denied
 *     ./login               read one guess per line on stdin, print one verdict
 *                           line each — this is the oracle the attacker drives.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <unistd.h>

/* Busy-work per matched byte. Stands in for a real per-byte cost (a crypto
 * round, a DB lookup, a network hop). It makes the ~1 ns real signal large
 * enough to survive scheduler + pipe noise in a live classroom. Set it to 0 and
 * raise the attacker's SAMPLES to prove the leak is real without the amplifier. */
#define WORK_PER_BYTE 60000

/* The secret. Only this program ever reads it. Change it and re-run. */
static const char *SECRET = "SomeRandomPassword123!@#";

/* volatile sink so -O2 cannot delete the busy loop */
static volatile uint64_t sink;

static void per_byte_work(void) {
    for (int k = 0; k < WORK_PER_BYTE; k++)
        sink += (uint64_t)k * 2654435761u;
}

#ifdef CONSTANT_TIME
/* ── THE FIX ──────────────────────────────────────────────────────────────
 * Compare EVERY byte, always. No early return, no data-dependent branch, the
 * same per-byte work every time. Runtime does not depend on how many leading
 * bytes matched, so the timing channel carries no information about the secret.
 * (Real code should call a vetted primitive: CRYPTO_memcmp, hmac.compare_digest,
 *  crypto/subtle.ConstantTimeCompare, crypto.timingSafeEqual.) */
static int check(const char *guess, size_t n) {
    size_t secret_len = strlen(SECRET);
    unsigned char diff = (unsigned char)((n ^ secret_len) != 0);  /* wrong length => fail */
    for (size_t i = 0; i < secret_len; i++) {
        unsigned char g = (i < n) ? (unsigned char)guess[i] : 0;
        diff |= (unsigned char)(g ^ (unsigned char)SECRET[i]);
        per_byte_work();                        /* ALWAYS — independent of the data */
    }
    return diff == 0;
}
#else
/* ── THE VULNERABILITY ────────────────────────────────────────────────────
 * Returns the instant it sees a wrong byte, so the number of leading bytes that
 * matched decides how long it runs. That runtime is an observable side channel.
 * This is exactly how naive password checks, memcmp(), and many token/MAC
 * comparisons behave. */
static int check(const char *guess, size_t n) {
    size_t secret_len = strlen(SECRET);
    if (n != secret_len) return 0;              /* wrong length: bail immediately */
    for (size_t i = 0; i < secret_len; i++) {
        if (guess[i] != SECRET[i]) return 0;    /* ← early exit: THIS is the leak */
        per_byte_work();
    }
    return 1;
}
#endif

int main(int argc, char **argv) {
    /* Classroom aid: announce the secret this process is guarding — on STDERR,
     * so the audience sees it on the console but it never enters the stdout pipe
     * the attacker reads. That's the whole point of the demo: the attacker
     * recovers THIS string without ever being told it. (A real login never does
     * this; here it lets the class watch the recovery converge on the answer.) */
    fprintf(stderr, "[login] guarding secret: \"%s\"  (%zu chars)\n",
            SECRET, strlen(SECRET));

    /* single-shot: the normal way you'd use a login on the command line */
    if (argc > 1) {
        int ok = check(argv[1], strlen(argv[1]));
        puts(ok ? "Access granted." : "Access denied.");
        return ok ? 0 : 1;
    }

    /* oracle mode: one guess per input line, one verdict per output line.
     * stdout to a pipe is fully buffered by default — force a flush per line so
     * the caller (attacker, or a human at the terminal) sees each reply at once. */
    setvbuf(stdout, NULL, _IOLBF, 0);
    int interactive = isatty(STDIN_FILENO);
    char line[256];
    for (;;) {
        if (interactive) { fputs("password: ", stderr); fflush(stderr); }
        if (!fgets(line, sizeof line, stdin)) break;   /* EOF */
        line[strcspn(line, "\n")] = '\0';              /* strip newline */
        int ok = check(line, strlen(line));
        puts(ok ? "Access granted." : "Access denied.");
        fflush(stdout);
    }
    return 0;
}
