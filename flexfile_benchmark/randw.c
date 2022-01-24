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


int main(int argc, char* argv[]) {
    if (argc != 4) return 0;

    int fd = open(argv[1], O_RDWR | O_CREAT, 0644);
    if (fd < 0) return 1;

    const u64 blksz = a2u64(argv[2]);
    const u64 filesz = a2u64(argv[3]);

    srandom_u64(time_nsec());
    u64 seq[filesz];
    for (u64 i=0; i<filesz; i++) {
        seq[i] = i * blksz;
    }
    shuffle_u64(seq, filesz);

    char *buf = malloc(blksz);
    for (u64 i=0; i<blksz; i++) {
        buf[i] = (u8)(i % 255);
    }

    u64 ot = time_nsec();

    for (u64 i=1; i<filesz+1; i++) {
        pwrite(fd, buf, blksz, seq[i-1]);
    }

    fsync(fd);

    printf("%f ops\n", filesz / (time_diff_nsec(ot) / (double)1e9));
    printf("%f MB/s\n", (filesz * blksz / 1048576) / (time_diff_nsec(ot) / (double)1e9));

    close(fd);

    free(buf);
    //remove(filename);
    return 0;
}
