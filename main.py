from function.Downloads import download_file

def main():
    print("Hello from blink-fetch-download-manager!")
    url = r"https://bits.avcdn.net/productfamily_ANTIVIRUS/insttype_FREE/platform_WIN/installertype_ONLINE/build_RELEASE/cookie_mmm_cnt_dlp_007_906_m"
    download_file(url)


if __name__ == "__main__":
    main()
