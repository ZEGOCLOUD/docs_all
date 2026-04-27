//
//  ViewController.h
//  ZegoDigitalHumanQuickStart
//
//  单文件实现 - 对齐Android的MainActivity.kt
//

#import <UIKit/UIKit.h>

NS_ASSUME_NONNULL_BEGIN

@class ZegoDigitalView;
@protocol IZegoDigitalMobile;

@interface ViewController : UIViewController

// UI组件
@property (nonatomic, strong) UILabel *tvStatus;
@property (nonatomic, strong) UILabel *tvRoomInfo;
@property (nonatomic, strong) UIView *digitalHumanContainerView;

// 数字人SDK实例
@property (nonatomic, strong, nullable) id<IZegoDigitalMobile> digitalMobile;

@end

NS_ASSUME_NONNULL_END
