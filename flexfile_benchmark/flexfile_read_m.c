#define _GNU_SOURCE

#include <fcntl.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <sys/time.h>
#include <errno.h>

#include "../c/lib.h"
#include "../flexfile.h"

struct read_ctx {
    struct flexfile *file;
    u64 blksz;
    u64 *start;
    u64 *end;
};

pthread_barrier_t start_barrier;
pthread_barrier_t end_barrier;
pthread_t workers[128];
struct read_ctx worker_ctxs[128];

void *read_worker(void *const octx)
{
    struct read_ctx *const ctx = octx;
    char *buf = malloc(ctx->blksz);
    u64 *off = ctx->start;
    pthread_barrier_wait(&start_barrier);
    while (off < ctx->end) {
        flexfile_read(ctx->file, buf, ctx->blksz * (*off), ctx->blksz);
        off++;
    }
    pthread_barrier_wait(&end_barrier);
    free(buf);
    return NULL;
}

int main(int argc, char* argv[]) {
    if (argc != 6) {
        printf("Usage: ./flexfile_read_m.out <path> <blksz> <filesz> <nthreads> <rand>\n");
        exit(1);
    }

    struct flexfile *ff = flexfile_open(argv[1]);
    if (!ff) return 1;

    const u64 blksz = a2u64(argv[2]);
    const u64 filesz = a2u64(argv[3]);
    const u64 nthreads = a2u64(argv[4]);
    const u64 rand = a2u64(argv[5]);

    srandom_u64(time_nsec());
    u64 *seq = malloc(filesz * sizeof(seq[0]));
    for (u64 i=0; i<filesz; i++) {
        seq[i] = i;
    }

    const u64 p = filesz / nthreads;
    if (rand) {
        for (u64 i=0; i<nthreads; i++) {
            shuffle_u64(seq+p*i, p);
        }
    }

    pthread_barrier_init(&start_barrier, NULL, nthreads+1);
    pthread_barrier_init(&end_barrier, NULL, nthreads+1);
    for (u64 i=0; i<nthreads; i++) {
        worker_ctxs[i] = (struct read_ctx)
                            { .file = ff, .blksz = blksz, .start=seq+p*i, .end=seq+p*i+p-1};
        pthread_create(&workers[i], NULL, read_worker, &worker_ctxs[i]);
    }

    u64 ot = time_nsec();
    pthread_barrier_wait(&start_barrier);
    pthread_barrier_wait(&end_barrier);
    printf("%f ops\n", filesz / (time_diff_nsec(ot) / (double)1e9));
    printf("%f MB/s\n", (filesz * blksz / 1048576) / (time_diff_nsec(ot) / (double)1e9));

    for (u64 i=0; i<nthreads; i++) {
        pthread_join(workers[i], NULL);
    }

    flexfile_sync(ff);
    flexfile_close(ff);

    free(seq);

    return 0;
}
