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
#include "../flextree.h"

#ifndef NR_EXTENTS_INSERT
#define NR_EXTENTS_INSERT (100000lu) // 10^5
#endif

#ifndef NR_EXTENTS_REGULAR
#define NR_EXTENTS_REGULAR (100000000lu) // 10^8
#endif

volatile u64 r = 0;

void insert()
{
    u64 *seq = malloc(sizeof(u64) * NR_EXTENTS_INSERT);
    seq[0] = 0;
    for (u64 i=1; i<NR_EXTENTS_INSERT; i++) {
        seq[i] = rand() % i;
    }
#ifdef ARRAY_TEST
    printf("sorted array test extents %lu\n", NR_EXTENTS_INSERT);
#else
#ifdef FLEXTREE_NAIVE
    printf("btree test extents %lu\n", NR_EXTENTS_INSERT);
#else
    printf("flextree test extents %lu\n", NR_EXTENTS_INSERT);
#endif
#endif
    fflush(stdout);
#ifdef ARRAY_TEST
    struct brute_force *index = brute_force_open(1);
#else
    struct flextree *index = flextree_open(NULL, 1);
#endif
    // insert
    u64 t = time_nsec();
    for (u64 i=0; i<NR_EXTENTS_INSERT; i++) {
#ifdef ARRAY_TEST
        brute_force_insert(index, seq[i], NR_EXTENTS_INSERT-1, 1);
#else
        flextree_insert(index, seq[i], NR_EXTENTS_INSERT-1, 1);
#endif
    }
    printf("--> insert %f mops/sec\n", (double)NR_EXTENTS_INSERT * 1e3 / time_diff_nsec(t));
    fflush(stdout);

#ifdef ARRAY_TEST
    brute_force_close(index);
#else
    flextree_close(index);
#endif
}

void regular() {
    u64 *seq = malloc(sizeof(u64) * NR_EXTENTS_REGULAR);
    for (u64 i=0; i<NR_EXTENTS_REGULAR; i++) {
        seq[i] = i;
    }
    shuffle_u64(seq, NR_EXTENTS_REGULAR);
    struct flextree_query_result *rr = malloc(65536); // 64K pretty enough!

#ifdef ARRAY_TEST
    printf("sorted array test extents %lu\n", NR_EXTENTS_REGULAR);
#else
#ifdef FLEXTREE_NAIVE
    printf("btree test extents %lu\n", NR_EXTENTS_REGULAR);
#else
    printf("flextree test extents %lu\n", NR_EXTENTS_REGULAR);
#endif
#endif
    fflush(stdout);

#ifdef ARRAY_TEST
    struct brute_force *index = brute_force_open(1);
#else
    struct flextree *index = flextree_open(NULL, 1);
#endif

    // append
    u64 t = time_nsec();
    for (u64 i=0; i<NR_EXTENTS_REGULAR; i++) {
#ifdef ARRAY_TEST
        brute_force_insert(index , i, NR_EXTENTS_REGULAR-i, 1);
#else
        flextree_insert(index, i, NR_EXTENTS_REGULAR-i, 1);
#endif
    }
    printf("--> append %f mops/sec\n", (double)NR_EXTENTS_REGULAR * 1e3 / time_diff_nsec(t));
    fflush(stdout);

    // query
    t = time_nsec();
    for (u64 i=0; i<NR_EXTENTS_REGULAR/10; i++) {
#ifdef ARRAY_TEST
        r += brute_force_pquery(index, seq[i]);
#else
        r += flextree_pquery(index, seq[i]);
#endif
    }
    printf("--> pquery %f mops/sec\n", (double)NR_EXTENTS_REGULAR * 1e3 / time_diff_nsec(t));
    fflush(stdout);

    // rquery
    t = time_nsec();
    for (u64 i=0; i<NR_EXTENTS_REGULAR/10; i++) {
#ifdef ARRAY_TEST
        brute_force_query_wbuf(index, seq[i], 50, rr);
#else
        flextree_query_wbuf(index, seq[i], 50, rr);
#endif
    }
    printf("--> rquery %f mops/sec\n", (double)NR_EXTENTS_REGULAR * 1e3 / time_diff_nsec(t));
    fflush(stdout);

#ifdef ARRAY_TEST
    brute_force_close(index);
#else
    flextree_close(index);
#endif

    free(seq);
    free(rr);
}

int main()
{
    insert();
    regular();
}
