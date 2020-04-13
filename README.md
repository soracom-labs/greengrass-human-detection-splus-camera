# Soracom Human Detection

This lambda is meant to be deployed on a greengrass enabled raspberry pi with a camera. The lambda will loop every 60 seconds to grab an image from the camera and send it to a SageMaker endpoint for inference. Specifically, we are using a [Human Detection](https://aws.amazon.com/marketplace/pp/prodview-3dr4kos6pq5cq) model from the AWS Marketplace that will return predictions about humans that are seen in the image. We then send this data and the image up to Soracom Harvest. 

## Getting Started

These instructions will get you a copy of the project up and running on your device for development and testing purposes. 

### Prerequisites

You will need to set up AWS Greengrass on your raspberry pi. Follow the [AWS Quick Start Guide](https://docs.aws.amazon.com/greengrass/latest/developerguide/quick-start.html) to do so. 

### Creating Lambda

Once Greengrass is set on your device, you are ready to create your lambda.

1. To create the Lambda function deployment package, save greegrassHumanDetection.py to a compressed zip file named greengrassHumanDetection.zip. The py file must be in the root of the directory.

    On UNIX-like systems (including the Mac terminal), you can use the following command to package the file and folder:

```
zip -r ../greegrass.zip .
```

2. Open the Lambda console and choose Create function.

3. Choose Author from scratch.

4. Name your function GreengrassHumanDetection, and set the remaining fields as follows:

    * For Runtime, choose Python 3.7.

    * For Permissions, keep the default setting. This creates an execution role that grants basic Lambda permissions. This role isn't used by AWS IoT Greengrass.

5. Choose Create function.

6. Upload your Lambda function deployment package:

    * On the Configuration tab, under Function code, set the following fields:

        * For Code entry type, choose Upload a .zip file.

        * For Runtime, choose Python 3.7.

        * For Handler, enter greengrassHumanDetection.function_handler

    * Choose Upload, and then choose greengrass.zip. (The size of your greengrass.zip file might be different from what's shown here.)

    * Choose Save.

7. The lambda function utilizes a Layer for numpy. Click Layers -> Add a layer. If `Select from list of runtime compatible layers` is toggled on, the SciPy layer will be recommended for you under Name. Select it and select the most recent version. Click save. 

8. Publish the Lambda function:

    * From Actions, choose Publish new version.

    * For Version description, enter First version, and then choose Publish.

9. Create an alias for the Lambda function version:

    * From Actions, choose Create alias.

    * Name the alias `mlTest`, set the version to `1` (which corresponds to the version that you just published), and then choose Create.

Now you can configure your Greengrass Group to use this lambda. Follow the [AWS Instructions](https://docs.aws.amazon.com/greengrass/latest/developerguide/config-lambda.html) making sure to select your lambda (`GreengrassHumanDetection`) and alias (`mlTest`). 

## Deployment

To deploy the lambda to your device, use the [AWS Instructions](https://docs.aws.amazon.com/greengrass/latest/developerguide/configs-core.html) for deployment. 

## Finally

If you log into your Soracom Console and select your devices SIM, you can select Actions -> Harvest Data. You will see the inference data populating here from your device. Naviagting to Harvest files, you will see the image uploaded by the device. 
