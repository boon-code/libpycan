#pragma once
#include <stdint.h>

/**************************************************
 * public definitions
 *************************************************/

#define CANFD_MAX_DLEN 64

#define PYCAN_RESULT_OK          0
#define PYCAN_RESULT_NOT_INIT    1
#define PYCAN_RESULT_ALREADY     2
#define PYCAN_RESULT_NULL_ARG    3
#define PYCAN_RESULT_NO_FRAME    4
#define PYCAN_RESULT_INCOMPLETE  5
#define PYCAN_RESULT_READ_ERROR  6
#define PYCAN_RESULT_WRITE_ERROR 7
#define PYCAN_RESULT_FAIL        8

/**************************************************
 * public structs
 *************************************************/

typedef struct {
	uint8_t major;
	uint8_t minor;
	uint8_t patch;
} VersionType;

// CAN frame

typedef uint32_t canid_t;

struct canfd_frame {
	canid_t can_id;  /* 32 bit CAN_ID + EFF/RTR/ERR flags */
	uint8_t    len;     /* frame payload length in byte */
	uint8_t    flags;   /* additional flags for CAN FD */
	uint8_t    __res0;  /* reserved / padding */
	uint8_t    __res1;  /* reserved / padding */
	uint8_t    data[CANFD_MAX_DLEN] __attribute__((aligned(8)));
};

typedef double can_timeout;

/**************************************************
 * public functions
 *************************************************/

extern int GetVersion(VersionType *version);

// CAN

extern int CanInitDefault(void);

extern int CanInit(
		const char * const interface,
		const char * const channel,
		const uint32_t bitrate);

extern int CanDeinit(void);

extern int CanRead(
		struct canfd_frame * const buffer,
		const size_t buffer_size,
		const can_timeout timeout,
		size_t * const n_frames_read);

extern int CanWrite(
		struct canfd_frame * const buffer,
		const size_t n_frames);

extern int CanTryWrite(
		struct canfd_frame * const buffer,
		const size_t n_frames,
		const can_timeout timeout,
		size_t * const n_frames_written);
