plugins {
    alias(libs.plugins.android.application)
    alias(libs.plugins.kotlin.android)
}

android {
    namespace = "com.example.digitalhumanquickstartdemo"
    compileSdk = 35

    defaultConfig {
        applicationId = "com.example.digitalhumanquickstartdemo"
        minSdk = 24
        targetSdk = 35
        versionCode = 1
        versionName = "1.0"

        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"

        // 从 local.properties 读取配置 / Read config from local.properties
        val appId = project.findProperty("ZEGO_APP_ID")?.toString() ?: "0"
        val apiBaseUrl = project.findProperty("ZEGO_API_BASE_URL")?.toString() ?: "http://localhost:3000"

        buildConfigField("long", "ZEGO_APP_ID", appId)
        buildConfigField("String", "ZEGO_API_BASE_URL", "\"$apiBaseUrl\"")
    }

    buildTypes {
        release {
            isMinifyEnabled = false
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
        }
        debug {
            isMinifyEnabled = false
        }
    }

    buildFeatures {
        buildConfig = true
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_11
        targetCompatibility = JavaVersion.VERSION_11
    }
    kotlinOptions {
        jvmTarget = "11"
    }
}

dependencies {
    // ZEGO 数字人SDK
    implementation("im.zego:digitalmobile:1.4.0.88")

    // ZEGO RTC SDK
    implementation("im.zego:express-private:3.22.0.46726")

    // 网络库
    implementation("com.squareup.okhttp3:okhttp:4.12.0")

    // JSON 解析
    implementation("com.google.code.gson:gson:2.10.1")

    // 图片加载
    implementation("com.github.bumptech.glide:glide:4.16.0")
    annotationProcessor("com.github.bumptech.glide:compiler:4.16.0")

    // Material Design
    implementation("com.google.android.material:material:1.11.0")

    // AndroidX
    implementation(libs.androidx.core.ktx)
    implementation(libs.androidx.lifecycle.runtime.ktx)
    implementation(libs.androidx.appcompat)

    // 测试相关
    testImplementation(libs.junit)
    androidTestImplementation(libs.androidx.junit)
    androidTestImplementation(libs.androidx.espresso.core)
}
