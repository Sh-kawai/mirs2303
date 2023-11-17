#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
#include <string.h>
#include <unistd.h>

#include "rplidar_sdk/sdk/include/sl_lidar.h" 
#include "rplidar_sdk/sdk/include/sl_lidar_driver.h"
#ifndef _countof
#define _countof(_Array) (int)(sizeof(_Array) / sizeof(_Array[0]))
#endif

using namespace sl;

static inline void delay(sl_word_size_t ms){
    while (ms>=1000){
        usleep(1000*1000);
        ms-=1000;
    };
    if (ms!=0)
        usleep(ms*1000);
}

bool ctrl_c_pressed;
void ctrlc(int)
{
    ctrl_c_pressed = true;
}

int main(int argc, char* argv)
{
    ///  Create a communication channel instance
    IChannel* _channel;
    _channel = (*createSerialPortChannel("/dev/ttyUSB0", 115200));
    ///  Create a LIDAR driver instance
    ILidarDriver * lidar = *createLidarDriver();
    auto res = (lidar)->connect(_channel);
    if(SL_IS_OK(res)){
        sl_lidar_response_device_info_t deviceInfo;
        res = (lidar)->getDeviceInfo(deviceInfo);
        if(SL_IS_OK(res)){
            printf("Model: %d, Firmware Version: %d.%d, Hardware Version: %d\n",
            deviceInfo.model,
            deviceInfo.firmware_version >> 8, deviceInfo.firmware_version & 0xffu,
            deviceInfo.hardware_version);
        }else{
            fprintf(stderr, "Failed to get device information from LIDAR %08x\r\n", res);
        }
    }else{
        fprintf(stderr, "Failed to connect to LIDAR %08x\r\n", res);
    }
    
    // ここから
    lidar->setMotorSpeed();

    // start scan...
    lidar->startScan(0,1);

    // fetech result and print it out...
    while (1) {
        sl_lidar_response_measurement_node_hq_t nodes[8192];
        size_t   count = _countof(nodes);

        res = lidar->grabScanDataHq(nodes, count);

        if (SL_IS_OK(res)) {
            lidar->ascendScanData(nodes, count);
            for (int pos = 0; pos < (int)count ; ++pos) {
                printf("%s theta: %03.2f Dist: %08.2f Q: %d \n", 
                    (nodes[pos].flag & SL_LIDAR_RESP_HQ_FLAG_SYNCBIT) ?"S ":"  ", 
                    (nodes[pos].angle_z_q14 * 90.f) / 16384.f,
                    nodes[pos].dist_mm_q2/4.0f,
                    nodes[pos].quality >> SL_LIDAR_RESP_MEASUREMENT_QUALITY_SHIFT);
            }
        }

        if (ctrl_c_pressed){ 
            break;
        }
    }

    lidar->stop();
	delay(200);
    lidar->setMotorSpeed(0);
    // done!
	
    /// Delete Lidar Driver and channel Instance
    delete lidar;
    delete _channel;
}