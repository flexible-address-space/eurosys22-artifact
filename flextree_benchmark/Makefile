# Makefile
# rules (always with .out)
# SRC-X.out += abc        # extra source: abc.c
# MOD-X.out += abc        # extra module: abc.c abc.h
# ASM-X.out += abc        # extra assembly: abc.S
# DEP-X.out += abc        # extra dependency: abc
# FLG-X.out += -finline   # extra flags
# LIB-X.out += abc        # extra -labc options

# X.out : xyz.h xyz.c # for extra dependences that are to be compiled/linked.

VPATH += .:../c/

# X => X.out
TARGETS += test
# X => X.c only
SOURCES +=
# X => X.S only
ASSMBLY +=
# X => X.c X.h
MODULES += ../c/lib ../generic ../flextree
# X => X.h
HEADERS +=

# EXTERNSRC/EXTERNDEP do not belong to this repo.
# extern-src will be linked
EXTERNSRC +=
# extern-dep will not be linked
EXTERNDEP +=

FLG +=
LIB += rt m

ifeq ($(ARRAY),y)
FLG += -DARRAY_TEST
else ifeq ($(BTREE),y)
FLG += -DFLEXTREE_NAIVE
endif

FLG += -DNR_EXTENTS_INSERT=$(INSERT) -DNR_EXTENTS_REGULAR=$(REGULAR)

include ../c/Makefile.common
