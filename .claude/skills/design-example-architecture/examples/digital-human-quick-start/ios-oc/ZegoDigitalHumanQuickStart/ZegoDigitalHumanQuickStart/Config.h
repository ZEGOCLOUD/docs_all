//
//  Config.h
//  ZegoDigitalHumanQuickStart
//
//  简单配置文件
//  Simple configuration file
//

#ifndef Config_h
#define Config_h

#import <Foundation/Foundation.h>

/**
 * 客户端配置 / Client configuration
 */
@interface Config : NSObject

// 从即构控制台获取: https://console.zego.im
// Get from ZEGO console: https://console.zegocloud.com
@property (class, nonatomic, readonly) NSUInteger ZEGO_APP_ID;

// 业务后台地址 / Backend API address
@property (class, nonatomic, readonly) NSString *ZEGO_API_BASE_URL;

@end

#endif /* Config_h */
