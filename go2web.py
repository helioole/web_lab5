import sys
import urllib.parse
import socket

def make_request(url):
    try:
        parsed_url = urllib.parse.urlparse(url)
        host = parsed_url.netloc
        path = parsed_url.path if parsed_url.path else '/'
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, 80))
            s.sendall(f"GET {path} HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n".encode())
            response = b""
            while True:
                data = s.recv(1024)
                if not data:
                    break
                response += data
            return response.decode()
    except Exception as e:
        print(f"Error executing web request: {e}")
        return None
    
def perform_search(keywords):
    try:
        url = f"https://www.google.com/search?q={urllib.parse.quote(' '.join(keywords))}"
        print("Search URL:", url)
        result = make_request(url)

        if result:
            print('\n'.join(result.split('\n')[:10]))
        else:
            print("Search failed.")
    except Exception as error:
        print(f"Уrror: {error}")

def print_help():
    print("""
Usage:
go2web -u <URL>         # make an HTTP request to the specified URL and print the response
go2web -s <search-term> # make an HTTP request to search the term using your favorite search engine and print top 10 results
go2web -h               # show this help
""")

def main():
    if len(sys.argv) < 2:
        print("Error: Missing arguments.")
        print_help()
        return
    
    option = sys.argv[1]
    
    if option == "-u" and len(sys.argv) == 3:
        url = sys.argv[2]
        response = make_request(url)
        if response:
            print(response)
    elif option == "-s" and len(sys.argv) > 2:
        search_terms = sys.argv[2:]
        perform_search(search_terms)
    elif option == "-h":
        print_help()
    else:
        print("Invalid option or missing arguments.")
        print_help()

if __name__ == "__main__":
    main()
