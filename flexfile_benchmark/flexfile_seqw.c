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

int main(int argc, char* argv[]) {
    if (argc != 4) return 0;

    struct flexfile *ff = flexfile_open(argv[1]);
    if (!ff) return 1;

    const u64 blksz = a2u64(argv[2]);
    const u64 filesz = a2u64(argv[3]);

    u64 seq[filesz];
    for (u64 i=0; i<filesz; i++) {
        seq[i] = i * blksz;
    }

    char *buf = malloc(blksz);
    for (u64 i=0; i<blksz; i++) {
        buf[i] = (u8)(i % 255);
    }

    u64 ot = time_nsec();

    for (u64 i=1; i<filesz+1; i++) {
        flexfile_insert(ff, buf, seq[i-1], blksz);
    }

    flexfile_sync(ff);

    printf("%f ops\n", filesz / (time_diff_nsec(ot) / (double)1e9));
    printf("%f MB/s\n", (filesz * blksz / 1048576) / (time_diff_nsec(ot) / (double)1e9));

    flexfile_close(ff);

    free(buf);
    //remove(filename);
    return 0;
}
