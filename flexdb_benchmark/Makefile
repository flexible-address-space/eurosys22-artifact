# Makefile
# rules (always with .out)
# SRC-X.out += abc        # extra source: abc.c
# MOD-X.out += abc        # extra module: abc.c abc.h
# ASM-X.out += abc        # extra assembly: abc.S
# DEP-X.out += abc        # extra dependency: abc
# FLG-X.out += -finline   # extra flags
# LIB-X.out += abc        # extra -labc options

# X.out : xyz.h xyz.c # for extra dependences that are to be compiled/linked.

VPATH += ..:../c/

# X => X.out
TARGETS +=
# X => X.c only
SOURCES +=
# X => X.S only
ASSMBLY +=
# X => X.c X.h
MODULES += ../c/lib ../c/kv ../c/ord ../c/wh ../generic ../flextree ../flexfile ../flexdb
# X => X.h
HEADERS +=

# EXTERNSRC/EXTERNDEP do not belong to this repo.
# extern-src will be linked
EXTERNSRC +=
# extern-dep will not be linked
EXTERNDEP +=

FLG +=
LIB += rt m uring

ifeq ($(LEVELDB),y)
	FLG += -DLEVELDB
	LIB += leveldb
endif
ifeq ($(ROCKSDB),y)
	FLG += -DROCKSDB
	LIB += rocksdb
endif
ifeq ($(LMDB),y)
	FLG += -DLMDB
	LIB += lmdb
endif
ifeq ($(KVELL),y)
	FLG += -DKVELL
	LIB += kvell
endif

ifneq ($(MAX_OFF),)
	FLG += -DFLEXFILE_MAX_OFFSET_OVERRIDE=$(MAX_OFF)
endif

include ../c/Makefile.common
