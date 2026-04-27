#!/usr/bin/env python3
"""
Script to update Xcode project.pbxproj for simplified single-file implementation.
This replaces the modular structure with Config.h/m and ViewController.h/m
"""

import hashlib
import random
import string

def generate_uuid():
    """Generate a 24-character hex string like Xcode uses."""
    return ''.join(random.choices(string.hexdigits.lower(), k=24))

def modify_project_file():
    project_file = "ZegoDigitalHumanQuickStart.xcodeproj/project.pbxproj"

    # Generate new UUIDs for our new files
    config_h_uuid = generate_uuid()
    config_m_uuid = generate_uuid()
    config_h_build_uuid = generate_uuid()
    config_m_build_uuid = generate_uuid()

    viewcontroller_h_uuid = generate_uuid()
    viewcontroller_m_uuid = generate_uuid()
    viewcontroller_m_build_uuid = generate_uuid()

    # Read the original file
    with open(project_file, 'r') as f:
        content = f.read()

    # Define the new sections
    new_build_file_section = f"""\t\t{config_m_build_uuid} /* Config.m in Sources */ = {{isa = PBXBuildFile; fileRef = {config_m_uuid} /* Config.m */; }};
\t\t{viewcontroller_m_build_uuid} /* ViewController.m in Sources */ = {{isa = PBXBuildFile; fileRef = {viewcontroller_m_uuid} /* ViewController.m */; }};"""

    new_file_ref_section = f"""\t\t{config_h_uuid} /* Config.h */ = {{isa = PBXFileReference; lastKnownFileType = sourcecode.c.h; path = Config.h; sourceTree = "<group>"; }};
\t\t{config_m_uuid} /* Config.m */ = {{isa = PBXFileReference; lastKnownFileType = sourcecode.c.objc; path = Config.m; sourceTree = "<group>"; }};
\t\t{viewcontroller_h_uuid} /* ViewController.h */ = {{isa = PBXFileReference; lastKnownFileType = sourcecode.c.h; path = ViewController.h; sourceTree = "<group>"; }};
\t\t{viewcontroller_m_uuid} /* ViewController.m */ = {{isa = PBXFileReference; lastKnownFileType = sourcecode.c.objc; path = ViewController.m; sourceTree = "<group>"; }};"""

    # First, remove all the old references from PBXBuildFile section (except essential ones)
    # Keep: AppDelegate.m, main.m, SceneDelegate.m
    # Remove: All ViewControllers, Models, Network, Utils, Views related build files

    # Find and replace PBXBuildFile section
    old_build_section_start = "/* Begin PBXBuildFile section */"
    old_build_section_end = "/* End PBXBuildFile section */"

    new_build_section = f"""/* Begin PBXBuildFile section */
\t\t{config_m_build_uuid} /* Config.m in Sources */ = {{isa = PBXBuildFile; fileRef = {config_m_uuid} /* Config.m */; }};
\t\t{viewcontroller_m_build_uuid} /* ViewController.m in Sources */ = {{isa = PBXBuildFile; fileRef = {viewcontroller_m_uuid} /* ViewController.m */; }};
\t\t92D9805A5E28C3005DDE9ED2 /* Pods_ZegoDigitalHumanQuickStart.framework in Frameworks */ = {{isa = PBXBuildFile; fileRef = D880F908AA7C02965DFC93BD /* Pods_ZegoDigitalHumanQuickStart.framework */; }};
\t\t9D76D71DA33A47B26186B0AE /* Foundation.framework in Frameworks */ = {{isa = PBXBuildFile; fileRef = A6F180BD737560F1FF02E81B /* Foundation.framework */; }};
\t\tCE72A13D3A40EAC907C2B872 /* main.m in Sources */ = {{isa = PBXBuildFile; fileRef = 8483E621F401E1E92D44E102 /* main.m */; }};
\t\t461E43F3D491A60E0A872DB4 /* AppDelegate.m in Sources */ = {{isa = PBXBuildFile; fileRef = DB147071CF9A65E6C81190BB /* AppDelegate.m */; }};
\t\tF956A185E0B413CF2FA61984 /* SceneDelegate.m in Sources */ = {{isa = PBXBuildFile; fileRef = 30138656593AB7522AEBDCB2 /* SceneDelegate.m */; }};
/* End PBXBuildFile section */"""

    # Replace PBXBuildFile section
    start_idx = content.find(old_build_section_start)
    end_idx = content.find(old_build_section_end, start_idx) + len(old_build_section_end)
    content = content[:start_idx] + new_build_section + content[end_idx:]

    # Find and replace PBXFileReference section
    old_file_ref_start = "/* Begin PBXFileReference section */"
    old_file_ref_end = "/* End PBXFileReference section */"

    new_file_ref_section = f"""/* Begin PBXFileReference section */
\t\t{config_h_uuid} /* Config.h */ = {{isa = PBXFileReference; lastKnownFileType = sourcecode.c.h; path = Config.h; sourceTree = "<group>"; }};
\t\t{config_m_uuid} /* Config.m */ = {{isa = PBXFileReference; lastKnownFileType = sourcecode.c.objc; path = Config.m; sourceTree = "<group>"; }};
\t\t{viewcontroller_h_uuid} /* ViewController.h */ = {{isa = PBXFileReference; lastKnownFileType = sourcecode.c.h; path = ViewController.h; sourceTree = "<group>"; }};
\t\t{viewcontroller_m_uuid} /* ViewController.m */ = {{isa = PBXFileReference; lastKnownFileType = sourcecode.c.objc; path = ViewController.m; sourceTree = "<group>"; }};
\t\t30138656593AB7522AEBDCB2 /* SceneDelegate.m */ = {{isa = PBXFileReference; includeInIndex = 1; lastKnownFileType = sourcecode.c.objc; name = SceneDelegate.m; path = ZegoDigitalHumanQuickStart/SceneDelegate.m; sourceTree = "<group>"; }};
\t\t618DFE9E0FD42AF0017B67C4 /* Pods-ZegoDigitalHumanQuickStart.debug.xcconfig */ = {{isa = PBXFileReference; includeInIndex = 1; lastKnownFileType = text.xcconfig; name = "Pods-ZegoDigitalHumanQuickStart.debug.xcconfig"; path = "Target Support Files/Pods-ZegoDigitalHumanQuickStart/Pods-ZegoDigitalHumanQuickStart.debug.xcconfig"; sourceTree = "<group>"; }};
\t\t780EDFD0F3E8273B2CC9BA0F /* AppDelegate.h */ = {{isa = PBXFileReference; includeInIndex = 1; lastKnownFileType = sourcecode.c.h; name = AppDelegate.h; path = ZegoDigitalHumanQuickStart/AppDelegate.h; sourceTree = "<group>"; }};
\t\t8483E621F401E1E92D44E102 /* main.m */ = {{isa = PBXFileReference; includeInIndex = 1; lastKnownFileType = sourcecode.c.objc; name = main.m; path = ZegoDigitalHumanQuickStart/main.m; sourceTree = "<group>"; }};
\t\tA6F180BD737560F1FF02E81B /* Foundation.framework */ = {{isa = PBXFileReference; lastKnownFileType = wrapper.framework; name = Foundation.framework; path = Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS18.0.sdk/System/Library/Frameworks/Foundation.framework; sourceTree = DEVELOPER_DIR; }};
\t\tC3C7363EAEBF05F32EC8A444 /* Pods-ZegoDigitalHumanQuickStart.release.xcconfig */ = {{isa = PBXFileReference; includeInIndex = 1; lastKnownFileType = text.xcconfig; name = "Pods-ZegoDigitalHumanQuickStart.release.xcconfig"; path = "Target Support Files/Pods-ZegoDigitalHumanQuickStart/Pods-ZegoDigitalHumanQuickStart.release.xcconfig"; sourceTree = "<group>"; }};
\t\tD880F908AA7C02965DFC93BD /* Pods_ZegoDigitalHumanQuickStart.framework */ = {{isa = PBXFileReference; explicitFileType = wrapper.framework; includeInIndex = 0; path = Pods_ZegoDigitalHumanQuickStart.framework; sourceTree = BUILT_PRODUCTS_DIR; }};
\t\tDB147071CF9A65E6C81190BB /* AppDelegate.m */ = {{isa = PBXFileReference; includeInIndex = 1; lastKnownFileType = sourcecode.c.objc; name = AppDelegate.m; path = ZegoDigitalHumanQuickStart/AppDelegate.m; sourceTree = "<group>"; }};
\t\tE290938A3B6DF41C38C6E913 /* ZegoDigitalHumanQuickStart.app */ = {{isa = PBXFileReference; explicitFileType = wrapper.application; includeInIndex = 0; path = ZegoDigitalHumanQuickStart.app; sourceTree = BUILT_PRODUCTS_DIR; }};
\t\tFEF5DCE59A611C5D68B01B56 /* SceneDelegate.h */ = {{isa = PBXFileReference; includeInIndex = 1; lastKnownFileType = sourcecode.c.h; name = SceneDelegate.h; path = ZegoDigitalHumanQuickStart/SceneDelegate.h; sourceTree = "<group>"; }};
/* End PBXFileReference section */"""

    start_idx = content.find(old_file_ref_start)
    end_idx = content.find(old_file_ref_end, start_idx) + len(old_file_ref_end)
    content = content[:start_idx] + new_file_ref_section + content[end_idx:]

    # Simplify PBXGroup section - remove Models, Network, Utils, Views groups
    old_group_start = "/* Begin PBXGroup section */"
    old_group_end = "/* End PBXGroup section */"

    new_group_section = """/* Begin PBXGroup section */
\t\t2F88EB29B40B744CC8E9CFDF /* Pods */ = {
\t\t\tisa = PBXGroup;
\t\t\tchildren = (
\t\t\t\tC3C7363EAEBF05F32EC8A444 /* Pods-ZegoDigitalHumanQuickStart.release.xcconfig */,
\t\t\t\t618DFE9E0FD42AF0017B67C4 /* Pods-ZegoDigitalHumanQuickStart.debug.xcconfig */,
\t\t\t);
\t\t\tpath = Pods;
\t\t\tsourceTree = "<group>";
\t\t};
\t\t4E3EE8542B46111B642A5B18 /* Products */ = {
\t\t\tisa = PBXGroup;
\t\t\tchildren = (
\t\t\t\tE290938A3B6DF41C38C6E913 /* ZegoDigitalHumanQuickStart.app */,
\t\t\t);
\t\t\tname = Products;
\t\t\tsourceTree = "<group>";
\t\t};
\t\t7F072805D2928A0909AB7B1C /* iOS */ = {
\t\t\tisa = PBXGroup;
\t\t\tchildren = (
\t\t\t\tA6F180BD737560F1FF02E81B /* Foundation.framework */,
\t\t\t);
\t\t\tname = iOS;
\t\t\tsourceTree = "<group>";
\t\t};
\t\tC3C3EFC47FAB2C70DAC85F3A /* Frameworks */ = {
\t\t\tisa = PBXGroup;
\t\t\tchildren = (
\t\t\t\t7F072805D2928A0909AB7B1C /* iOS */,
\t\t\t\tD880F908AA7C02965DFC93BD /* Pods_ZegoDigitalHumanQuickStart.framework */,
\t\t\t);
\t\t\tname = Frameworks;
\t\t\tsourceTree = "<group>";
\t\t};
\t\tEAA1FE37556BD1E7CB38B9E9 = {
\t\t\tisa = PBXGroup;
\t\t\tchildren = (
\t\t\t\t4E3EE8542B46111B642A5B18 /* Products */,
\t\t\t\tC3C3EFC47FAB2C70DAC85F3A /* Frameworks */,
\t\t\t\tF73A3DC881CD8D6802D8CE47 /* ZegoDigitalHumanQuickStart */,
\t\t\t\t2F88EB29B40B744CC8E9CFDF /* Pods */,
\t\t\t);
\t\t\tsourceTree = "<group>";
\t\t};
\t\tF73A3DC881CD8D6802D8CE47 /* ZegoDigitalHumanQuickStart */ = {
\t\t\tisa = PBXGroup;
\t\t\tchildren = (
\t\t\t\t780EDFD0F3E8273B2CC9BA0F /* AppDelegate.h */,
\t\t\t\tFEF5DCE59A611C5D68B01B56 /* SceneDelegate.h */,
\t\t\t\t{config_h_uuid} /* Config.h */,
\t\t\t\t{viewcontroller_h_uuid} /* ViewController.h */,
\t\t\t\tDB147071CF9A65E6C81190BB /* AppDelegate.m */,
\t\t\t\t{config_m_uuid} /* Config.m */,
\t\t\t\t{viewcontroller_m_uuid} /* ViewController.m */,
\t\t\t\t8483E621F401E1E92D44E102 /* main.m */,
\t\t\t\t30138656593AB7522AEBDCB2 /* SceneDelegate.m */,
\t\t\t\t51B0A0BB5E168564623FF2AE /* Info.plist */,
\t\t\t);
\t\t\tname = ZegoDigitalHumanQuickStart;
\t\t\tsourceTree = "<group>";
\t\t};
/* End PBXGroup section */"""

    start_idx = content.find(old_group_start)
    end_idx = content.find(old_group_end, start_idx) + len(old_group_end)
    content = content[:start_idx] + new_group_section + content[end_idx:]

    # Update PBXSourcesBuildPhase section
    old_sources_start = "/* Begin PBXSourcesBuildPhase section */"
    old_sources_end = "/* End PBXSourcesBuildPhase section */"

    new_sources_section = f"""/* Begin PBXSourcesBuildPhase section */
\t\tD7C350486BD0F0E64BFBE7BB /* Sources */ = {{
\t\t\tisa = PBXSourcesBuildPhase;
\t\t\tbuildActionMask = 2147483647;
\t\t\tfiles = (
\t\t\t\t{config_m_build_uuid} /* Config.m in Sources */,
\t\t\t\t{viewcontroller_m_build_uuid} /* ViewController.m in Sources */,
\t\t\t\tCE72A13D3A40EAC907C2B872 /* main.m in Sources */,
\t\t\t\t461E43F3D491A60E0A872DB4 /* AppDelegate.m in Sources */,
\t\t\t\tF956A185E0B413CF2FA61984 /* SceneDelegate.m in Sources */,
\t\t\t);
\t\t\trunOnlyForDeploymentPostprocessing = 0;
\t\t}};
/* End PBXSourcesBuildPhase section */"""

    start_idx = content.find(old_sources_start)
    end_idx = content.find(old_sources_end, start_idx) + len(old_sources_end)
    content = content[:start_idx] + new_sources_section + content[end_idx:]

    # Write the modified content
    with open(project_file, 'w') as f:
        f.write(content)

    print(f"✅ Updated {project_file} successfully!")
    print("New files added: Config.h, Config.m, ViewController.h, ViewController.m")
    print("Old modular files removed from project references")

if __name__ == "__main__":
    import os
    os.chdir("/Users/oliver/Downloads/tmp/docs_all_digital_human/sample-code/ios-oc/ZegoDigitalHumanQuickStart")
    modify_project_file()
