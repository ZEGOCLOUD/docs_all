## 常见问题

**Android 示例源码运行时，如果报错 “Unrecognized option: --add-opens=java.base/java.io=ALL-UNNAMED”，该如何处理？**

![/Pics/GoEnjoy/AS_ALL_UNNAMED.png](https://doc-media.zego.im/sdk-doc/Pics/GoEnjoy/AS_ALL_UNNAMED.png)

有两种解决方案：

- 升级 Android Studio 至最新版本，重新运行即可。

- 找到项目的 gradle.properties 文件，删除 `--add-opens=java.base/java.io=ALL-UNNAMED` 并保存，重新运行即可。

    ![/Pics/GoEnjoy/AS_ALL_UNNAMED_delete.png](https://doc-media.zego.im/sdk-doc/Pics/GoEnjoy/AS_ALL_UNNAMED_delete.png)




