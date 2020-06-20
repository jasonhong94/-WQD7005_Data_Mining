Part 2 Mobile App
The Android mobile application was created by using Android Studio.

Inside the app/src/main/res/layout/activity_main.xml, under the Palette section, we created a WebView. We set the properties of webview with both height and width to be “fill_parent’.

Under the ‘MainActivity.java’, we created a private class for WebView, which is under the public class MainActivity.
image The webview will load the url from our web application.

Under the AndroidManifest.xml, we added the user permission with internet permission inside the xml

To make sure the app is suitable with any screen size, we added the following properties image



