# wwdc-sessions-downloader
For Apple WWDC session videos download.


## Features

- [x]  download all session videos of specified year
- [x]  chose HD or SD video quality
- [x]  download pdf file if exits
- [ ]  download specified session video


## Example

download all 2022 wwdc session videos in hd quality.

```shell
# download wwdc 2022 all hd videos not pdfs
python3 main.py ---year=2022

# download wwdc 2022 all hd videos not pdfs
python3 main.py ---year=2022 --quality=sd

# download wwdc 2015 all sd videos with pdf
python3 main.py ---year=2015 --quality=sd --pdf
```

## Params

| param | value | desc |
| ------------- | ------------- | ------------- |
| year  | int  | Determine which year of wwdc  |
| path  | string  | ideo save path.default is current.  |
| quality  | {hd,sd}  | Video quality support HD and SD. Default is SD.  |
| queue_count  | int  | Video download queue count. Default is 3  |
| pdf  | --  | Should download pdf if exists.  |



## Author

huiping_guo, huiping192@gmail.com

## License

wwdc-sessions-downloader is available under the MIT license. See the LICENSE file for more info.
