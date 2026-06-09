# 移动端 UI 基础可用性要求

本参考用于 Android、iOS、HarmonyOS、Flutter、React Native、uni-app 等移动端或移动容器 demo 的 UI 编写。它约束 demo 的最低可用性，不属于额外美化。

## 虚拟键盘避让

只要页面包含可聚焦输入控件，尤其是底部聊天输入栏、评论框、表单提交栏、搜索框，就必须处理虚拟键盘避让：

- 键盘弹出后，当前输入框必须仍然可见。
- 与输入框配套的发送、提交、确认按钮必须仍然可见且可点击。
- 不要把输入栏用固定坐标或不可 resize 的绝对定位钉在屏幕底部。
- 页面主体应允许随窗口或键盘高度变化而 resize、滚动或调整底部 inset。
- 底部输入区应考虑 safe area、导航栏和手势区域。

## 平台实现提示

### Android 原生

- 在 Activity 或 Manifest 中设置合适的软键盘策略，优先使用 `adjustResize`。
- 根布局避免固定死高度；聊天区、列表区应在输入栏上方占据可伸缩空间。
- 底部输入栏应随可用窗口高度变化上移，不要被 IME 覆盖。
- 如果使用全屏、沉浸式或 edge-to-edge，需要显式处理 ime/window insets。

### iOS 原生

- 监听 keyboard show/hide，调整底部约束、scroll view inset 或输入栏容器约束。
- 同时处理 safe area，避免输入栏贴到 Home Indicator 区域。
- 聊天列表或表单内容应在键盘弹出后仍可滚动到当前输入位置。

### HarmonyOS

- 使用系统推荐的键盘避让能力，或监听键盘高度调整输入栏和滚动容器。
- 输入栏不要固定在屏幕底部不随键盘变化。
- 页面底部需要考虑系统导航区、安全区和软键盘区域。

### Flutter

- 使用 `Scaffold(resizeToAvoidBottomInset: true)` 或等效方案。
- 避免把底部输入栏放在不会响应 `viewInsets.bottom` 的固定 `Stack` 位置。
- 必要时使用 `SafeArea`、`MediaQuery.viewInsets.bottom`、可滚动容器或约束布局。

### React Native

- 使用 `KeyboardAvoidingView` 或等效键盘避让方案。
- iOS 和 Android 可分别设置合适的 `behavior` / offset。
- 底部输入栏应在避让容器内，避免被绝对定位遮挡。

### uni-app / Web 移动端

- 使用平台提供的键盘高度、viewport resize 或 safe-area 方案调整输入区。
- 固定底部输入栏时必须结合键盘高度或 visual viewport 变化更新位置。
- 在移动 WebView 中避免只依赖桌面浏览器的固定定位行为。

## 代码归因

如果 demo 没有处理键盘避让，优先归类为 `🔧 代码实现问题`，因为这是移动端 demo 的基础可用性要求。

只有当目标文档明确提供了 UI 示例，并且该示例本身要求或展示了会导致输入框被键盘遮挡的错误布局时，才关联为 `📄 文档问题`。
