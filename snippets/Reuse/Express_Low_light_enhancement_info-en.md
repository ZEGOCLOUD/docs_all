Low-light enhancement refers to the function of enhancing the brightness of the captured image when the ambient light is dark and the brightness of the image captured by the camera does not meet the business requirements, such as recognizing the face of the communication partner or performing face recognition.

ZEGOCLOUD provides two ways of low-light enhancement:

- Method 1: By enabling adaptive frame rate, dynamically reduce the capture frame rate within the set frame rate range to extend the exposure time of each frame and enhance the brightness of the captured image. For example, developers enable and set the adaptive frame rate range to [10, 25]. When the ambient light is sufficient, the capture frame rate is still 25 frames, and when the ambient light is low, the capture frame rate will dynamically adjust between [10, 25] to extend the exposure time of each frame and enhance the brightness of the captured image.

- Method 2: Enhance the brightness of the captured image through algorithms:
    - Manual enhancement mode: Determine whether to enable algorithm enhancement based on the received parameters.
    - Automatic enhancement mode: The SDK automatically determines whether to enable algorithm enhancement and the degree of enhancement based on the ambient light intensity in which the user is located.

Both processing methods can be used independently or simultaneously and are compatible with the beauty function.

### Advantages

- Full model coverage.
- Support multiple modes, flexible selection according to business needs.
- Small system resource usage.

### Effect demonstration

|Before Enhancement|After Enhancement|
|-|-|
|![https://doc-media.zego.im/sdk-doc/Pics/lowlightenhancement/lowlightenhancement_before.jpg](https://doc-media.zego.im/sdk-doc/Pics/lowlightenhancement/lowlightenhancement_before.jpg)| ![https://doc-media.zego.im/sdk-doc/Pics/lowlightenhancement/lowlightenhancement_after.jpg](https://doc-media.zego.im/sdk-doc/Pics/lowlightenhancement/lowlightenhancement_after.jpg)|




