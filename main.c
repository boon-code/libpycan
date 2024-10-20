#include <stdlib.h>
#include <stdio.h>
#include <assert.h>
#include "libpycan.h"

int main(void)
{
	VersionType v = {0};
	printf("Before ...\n");
	uint8_t ret = GetVersion(&v);
	printf("GetVersion result: %d\n", ret);
	printf("Version %hhu.%hhu.%hhu\n", v.major, v.minor, v.patch);

	struct canfd_frame frame;
	size_t n_frames = 0;

	ret = CanInitDefault();
	printf("CanInit result: %d\n", ret);
	assert((ret == PYCAN_RESULT_OK) && "not init");

	ret = CanRead(&frame, 1, 2.0, &n_frames);
	printf("CanRead result: %d\n", ret);

	if (ret != PYCAN_RESULT_OK) {
		frame.can_id = 0x100;
		frame.len = 8;
		frame.data[0] = 0;
		frame.data[1] = 1;
		frame.data[2] = 2;
		frame.data[3] = 3;
		frame.data[4] = 4;
		frame.data[5] = 5;
		frame.data[6] = 6;
		frame.data[7] = 7;
	}
	frame.can_id += 1; // easier to see

	ret = CanTryWrite(&frame, 1, 2.0, &n_frames);
	printf("CanTryWrite result: %d\n", ret);

	frame.can_id += 1;
	ret = CanWrite(&frame, 1);
	printf("CanWrite result: %d\n", ret);

	return EXIT_SUCCESS;
}
