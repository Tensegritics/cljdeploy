# Deploy your ClojureDart application

This is an example repository containing the scripts necessary to deploy an iOS & Anrdoid app to the stores.

These scripts depend on Github Actions (and taht's where all secretes are stored). They can be used either by Github servers or by a Github Actions runner running locally on one of your machines (faster and cheaper builds, especially for macOS). 

Bexware: they have only been tested on macOs.

PR are welcomed if you want to add a deployment target (Windows, web, macOs...)

### Structure of the project

### iOS

iOS script is fully contained in `.github/workflows/preview-ios.yml`, just fill in appropriate values.
After setting Apple Store Connect up you only have to tag your branch with a `preview-ios*` prefix.

### Android

Android is a little bit more complicated. Script is also hosted in `.github/workflows/preview-android.yml` (and you still have to fill appropriate values) but there are 2 additional scripts, one for fetching the appliction release number and the other to upload the app. Both scripts are located in `deploy` -- they have to be modified too.

Don't forget to amend your `android/app/build.gradle`, specialy the `signingConfigs` configuration, see the highlighted parts in the example in the `android/app/build.gradle` of this project.

## Running CI

After configuring iOS & Android, configure your selfhost runner https://github.com/teamid/projectname/settings/actions/runners and tag & push your branch. It will trigger the CI.
