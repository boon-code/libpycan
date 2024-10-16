#pragma once
#include <stdint.h>

typedef struct {
	uint8_t major;
	uint8_t minor;
	uint8_t patch;
} VersionType;

extern uint8_t GetVersion(VersionType *version);

