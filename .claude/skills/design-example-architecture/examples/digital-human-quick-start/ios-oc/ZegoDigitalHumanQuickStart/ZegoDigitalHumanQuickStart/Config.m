//
//  Config.m
//  ZegoDigitalHumanQuickStart
//
//  简单配置文件 / Simple configuration file
//

#import "Config.h"

@implementation Config

+ (NSUInteger)ZEGO_APP_ID {
    // 从即构控制台获取: https://console.zego.im
    // Get from ZEGO console: https://console.zegocloud.com
    return 1234567890;
}

+ (NSString *)ZEGO_API_BASE_URL {
    return @"http://localhost:3000";
}

@end
