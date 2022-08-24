# wwdc-sessions-downloader
For Apple WWDC session videos download.


## Features

- [x]  download all session videos of specified year
- [x]  chose HD or SD video quality
- [x]  download pdf file if exits
- [x]  download specified session video


## Usage

Clone the project.
```
git clone https://github.com/huping192/wwdc-sessions-downloader
```

Install packages.
```
python3 -m pip install -r requirements.txt --user
```

Run python script
```
python3 main.py --year=2022
```

## Example

### download all wwdc session videos.

```shell
# download wwdc 2022 all sd videos not pdfs
python3 main.py --year=2022
python3 main.py --y=2022


# download wwdc 2022 all hd videos not pdfs
python3 main.py --year=2022 --quality=hd
python3 main.py -y=2022 -q=hd

# download wwdc 2015 all sd videos with pdf
python3 main.py --year=2015 --quality=sd --pdf
python3 main.py -y=2015 --q=sd --pdf

```


### download specified wwdc session video.

```shell
# download wwdc 2015 session 508 sd video
python3 main.py --year=2015 --session=508
python3 main.py -y=2015 -s=508

# download wwdc 2015 session 508 hd video
python3 main.py --year=2015 --session=508 --quality=hd
python3 main.py -y=2015 -s=508 -q=hd

# download wwdc 2015 session 508 sd video with pdf
python3 main.py ---year=2015 --session=508 --pdf
python3 main.py -y=2015 -s=508 --pdf

```

## Params

| param | short param | value | desc |
| ------------- | ------------- | ------------- | ------------- |
| year  | y  | int  | Determine which year of wwdc  |
| session  | s  | string  | Determine which session to download. Download all sessions if not specified. |
| path  | p  | string  | video save path.default is current dic.  |
| quality  | q  | {hd,sd}  | Video quality support HD and SD. Default is SD.  |
| queue_count  | qc  | int  | Video download queue count. Default is 3  |
| pdf  | pdf  | --  | Should download pdf if exists.  |



## Author

huiping_guo, huiping192@gmail.com

## License

wwdc-sessions-downloader is available under the MIT license. See the LICENSE file for more info.
