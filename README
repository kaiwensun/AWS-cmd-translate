## AWS cmd translate

This is a command line translation tool backed by [Amazon Translate](https://aws.amazon.com/translate/)

### Prerequesites

* Python3
* An AWS account
* Set up an AWS account profile (eg. [AWS Config File](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html#aws-config-file))
* Download this repository to your local machine.

### Usage

#### Installation
* On the first time run of `translate.sh`, installation will run.
* If you want to install without translating anything, run `./script/build.sh`.

#### Translation
* One-time mode:
```
$ ./translate.sh I want to translate this sentence.
```
* Standby mode:
```
$ ./translate.sh
> 爱笑的人运气不会太差。
Luck for those who love to laugh will not be too bad.
> Comment ça va?
你好吗？
> 你好吗？
How are you?
```
* You can add `./translate.sh`'s folder to your `PATH` environment variable for faster access.

#### Special commands
Special commands are available in standby mode.
* `exit` - exit the program. Of course you can always use `Ctrl + C` to exit.
* `clear` or `cls` - clear the screen

#### Configuration

If your main language is not (Simplified) Chinese, you can your own from [Amazon Translate supported languages](https://docs.aws.amazon.com/translate/latest/dg/what-is.html#what-is-languages).

Then create a file `./config/local_settings.py` and override the `MAIN_LANGUAGE` with your language code there. For example,

```
# ./config/local_settings.py
MAIN_LANGUAGE = "ko"
```