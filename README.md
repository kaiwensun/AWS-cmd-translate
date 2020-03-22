# AWS cmd translate

This is a command line translation tool backed by [Amazon Translate](https://aws.amazon.com/translate/) and Youdao.

## Prerequesites

* Python3
* An AWS account
* Set up an AWS account profile (eg. [AWS Config File](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html#aws-config-file))
* Download this repository to your local machine.

## Usage

### Installation
* On the first time run of `translate.sh`, installation will run.
* If you want to install without translating anything, run `./script/build.sh`.

### Translation
#### One-time mode:
```
$ ./translate.sh I want to translate this sentence.
```
#### Standby mode:
```
$ ./translate.sh
> 爱笑的人运气不会太差。
Luck for those who love to laugh will not be too bad.
> Comment ça va?
你好吗？
> 你好吗？
How are you?
```
#### Faster access
You can add `./translate.sh`'s folder to your `PATH` environment variable for faster access.

### Special commands
Special commands are available in standby mode.
* `exit` - exit the program. Of course you can always use `Ctrl + C` to exit.
* `clear` or `cls` - clear the screen

### Configurations

#### Main language
If your main language is not (Simplified) Chinese, you can choose your own language code from [Amazon Translate supported languages](https://docs.aws.amazon.com/translate/latest/dg/what-is.html#what-is-languages).

Then create a file `./config/local_settings.py` and override the `MAIN_LANGUAGE` with your language code there. For example,

```
# ./config/local_settings.py
MAIN_LANGUAGE = "ko"
```

Then you can try

```
$ ./translate.sh how are you?
잘 지내세요?
```

### Advanced Configurations

#### AWS Translate client
A few common aws client configuration (such as region and secret access key) can be overridden in `config/local_settings.py` file. Check `config/settings.py` for details.

#### Integrate with other dictionaries
To integrate with your own dictionary engines, you can create your own Python class under the `translators` folder. The class should have `lookup` and `display` methods. Then override the `ENGINES`. For example, to use Amazon Translate only when Youdao translator is not available,

```
# config/local_settings.py
ENGINES = [
    "Youdao",
    "AmazonTranslate"
]
ONLY_ONE_ENGINE = True
```

### Youdao Dictionary (1.1)

A deprecated version of [Youdao translation API](http://fanyi.youdao.com/openapi?path=data-mode) is integrated with this tool. If you have registered an API key before it was deprecated, you can put them in the `config/local_settings.py`, and add `"Youdao"` in the `ENGINES` settings.

```
YOUDAO_APP_NAME = "your app name here"
YOUDAO_API_KEY = "your api key here"
```

Example user experience:

```
$ ./translate.sh
> 直升机
=========== youdao ============
[zhí shēng jī]
helicopter
copter
The helicopter

直升机
 - Helicopter
 - copter
 - Chopper Checkpoint

军用直升机
 - military helicopter
 - military helicopter
 - Army Helicopters

直升机航母
 - helicopter carrier
 - CVH
====== amazon_translate =======
直升机
> helicopter
=========== youdao ============
[ˈhelɪkɒptə(r)]
n. [航] 直升飞机
vt. 由直升机运送
vi. [航] 乘直升飞机
直升机

Helicopter
 - 直升机
 - 直升飞机
 - 直升

helicopter parents
 - 直升机父母
 - 直升机家长
 - 指某些“望子成龙

Helicopter Theory
 - 直升机理论
 - 直升飞机理论
 - 原名
====== amazon_translate =======
直升机
> 大风车吱呀吱悠悠的转
=========== youdao ============
Large wind turbines, noting cheep turn leisurely
====== amazon_translate =======
Big windmill squeaky turn
> Comment ça va?
=========== youdao ============
怎么样?
====== amazon_translate =======
你好吗？
> ça va!
=========== youdao ============
你好!
====== amazon_translate =======
查瓦！
```