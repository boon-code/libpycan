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

	ret = CanInit("virtual", "test-channel", 500000U);
	printf("CanInit result: %d\n", ret);
	assert((ret == PYCAN_RESULT_OK) && "not init");

	ret = CanRead(&frame, 1, 2.0, &n_frames);
	printf("CanRead result: %d\n", ret);

	return EXIT_SUCCESS;
}
