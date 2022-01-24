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

    char *buf = malloc(blksz);
    for (u64 i=0; i<blksz; i++) {
        buf[i] = (u8)(i % 255);
    }

    for (u64 i=0; i<filesz; i++) {
        write(fd, buf, blksz);
    }

    fsync(fd);
    close(fd);

    free(buf);
    //remove(filename);
    return 0;
}
