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

struct read_ctx {
    int fd;
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
        pread(ctx->fd, buf, ctx->blksz, ctx->blksz * (*off));
        off++;
    }
    pthread_barrier_wait(&end_barrier);
    free(buf);
    return NULL;
}

int main(int argc, char* argv[]) {
    if (argc != 6) {
        printf("Usage: ./read_m.out <path> <blksz> <filesz> <nthreads> <rand>\n");
        exit(1);
    }

    int fd = open(argv[1], O_RDWR | O_CREAT, 0644);
    if (fd < 0) return 1;

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
                            { .fd = fd, .blksz = blksz, .start=seq+p*i, .end=seq+p*i+p-1};
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

    fsync(fd);
    close(fd);

    free(seq);

    return 0;
}
