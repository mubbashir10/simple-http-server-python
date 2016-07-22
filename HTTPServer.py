#########################################
# Mubbashir Mustafa                     #
# http://mubbashir10.com                #
# mubbashir10@gmail.com                 # 
#########################################

#importing required libraries
import socket
import re
import thread
import time

#defining host
host = 'localhost'

#defining port number
port = 13555

#making TCP connection
listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

#opening socket
listen_socket.bind((host, port))

#starting listening to clients (maximum 5 clients in queue are allowed)
listen_socket.listen(5)

#printing success message
print '\nServer Status:\nStarting Virtual Server...\nServing HTTP on port no. %s' %port

#creating server funtionality
def server_data(pseudo_int):

    #accepting client requests
    while True:

        #accepting client data
        client_connection, client_address = listen_socket.accept()
        print'\nNow Serving: '
        print client_address

        #getting client requests
        client_requests = client_connection.recv(1024)

        #printing client requests
        print '\nClient Requests:\n'+client_requests

        #only continue execution if the request is recieved
        if client_requests:

            #parsing client requests to get current url
            requests = client_requests.split('\n')
            current_url_raw_1 = requests[0]
            current_url_raw_1_array = current_url_raw_1.split('GET /')
            current_url_raw_2= current_url_raw_1_array[1]
            current_url_raw_2_array = current_url_raw_2.split(' ')
            current_url = current_url_raw_2_array[0]

            #creating dynamic page (homepage)
            if current_url=='':
                message = """\
    HTTP/1.1 200 OK

    <html><head><title>Welcome - CN Project</title><link rel="icon" href="data:;base64,iVBORw0KGgo="></head><body><h1 style="font-family:arial; font-size:45px; color:#191919; margin-top:200px; text-align:center">Coming Soon</h1><h2 style="font-family:arial; font-size:20px; color:#c1c1c1; margin-top:10px; text-align:center">we are working on our website, it will be up soon!</h2></body></html>
    """
            
            #creating dynamic page (ChessBoard)
            elif re.match(r'(ChessBoard_x)(\d+)(_y)(\d+)(.bmp)', current_url, re.IGNORECASE):

                #calculating size (width x height) of the bitmap imag
                cheesboard_url_raw = current_url.split('_')
                print 'Size(x) and Height(y):'

                #getting x value
                x_value = cheesboard_url_raw[1]
                width = re.findall(r'\d+', x_value) 
                print 'x = %s'%width[0]

                #getting y value
                y_value = cheesboard_url_raw[2]
                height = re.findall(r'\d+', y_value) #final value of y
                print 'y = %s'%height[0]

                #creating bitmap image
                def bitmap_creator(rows): 

                    #Bitmap Identifier
                    bm_identifier = "BM"

                    #Bitmap File Size
                    file_size = "\x40\x00\x0c\x00"

                    #Reserved (Unused) bits
                    reserved = "\x00\x00" "\x00\x00"

                    #File Offset
                    offset = "\x36\x00\x00\x00" 

                    #No. of Bytes in DIB header   
                    dib_header = "\x28\x00\x00\x00"

                    #Width of Bitmap
                    bmp_width = "\x00\x02\x00\x00" 

                    #Height of Bitmap
                    bmp_height = "\x00\x02\x00\x00" 

                    #Color Planes
                    color_planes = "\x01\x00" 

                    #Bits per Pixel 
                    bits_per_pixel = "\x18\x00" 

                    #Compression level
                    compression = "\x00\x00\x00\x00" 

                    #Size Raw Data
                    raw_data_size = "\x10\x00\x00\x00" 

                    #Horizontal Resolution
                    res_x = "\x13\x0B\x00\x00" 

                    #Vertical Resolution
                    res_y = "\x13\x0B\x00\x00"

                    #Number of Colors in Palette
                    color_palette = "\x00\x00\x00\x00" 

                    #Important Colors
                    imp_color = "\x00\x00\x00\x00"

                    #generating Bitmap Header
                    bitmap_header = bm_identifier + file_size + reserved + offset + dib_header + bmp_width + bmp_height + color_planes + bits_per_pixel + compression + raw_data_size + res_x + res_y + color_palette + imp_color
                    
                    #converting bitmap pixel array in bytes array
                    bitmap_data = b"".join([bytes(row) for row in reversed(rows)])+" "

                    #creating bitmap image
                    bitmap_image = bitmap_header + bitmap_data

                    #returning bitmap image
                    return (bitmap_image);

                #checking size validity (x and y should be equal and must divide 512 completely)
                if(width[0]==height[0]) & (512%(int(width[0])) == 0) & ((int(width[0])) <= 512):
                    
                    #defining size of the block
                    size = (int(width[0]));

                    #assigning flags to colors
                    black = True;
                    white = False;

                    #defining initial rows and columns
                    row = 0;
                    count = 0;

                    #creating pixels array with all white boxes
                    bitmap_pixels_array= ["\xff\xff\xff" for x in range(512*512)]

                    #if size is 512 then return image with single white block
                    if(size==512):

                        message = (bitmap_creator(bitmap_pixels_array))

                    #if size is less than 512 then fill image with pattern      
                    else:
                        
                        #filling boxes with alternate pattern (white, black)
                        for i in range (512*512):
                            if(black):
                                bitmap_pixels_array[i]="\x00\x00\x00"
                            elif(white):
                                bitmap_pixels_array[i]="\xff\xff\xff"

                            #incrementing count by 1    
                            count+=1

                            #swapping white and black for next row
                            if(count%size==0):
                                temp = black
                                black = white
                                white = temp

                            #start new row and swap colors    
                            if(i%512==0):
                                row+=1
                                if(row%size==0):
                                    temp=black
                                    black=white
                                    white=temp

                        #sending bitmap image          
                        message = (bitmap_creator(bitmap_pixels_array))

                else:
                    message = """\
    HTTP/1.1 403 Forbidden

    <html><head><title>Error - CN Project</title><link rel="icon" href="data:;base64,iVBORw0KGgo="></head><body><h1 style="font-family:arial; font-size:45px; color:#191919; margin-top:200px; text-align:center">Invalid Size Error!</h1><h2 style="font-family:arial; font-size:20px; color:#c1c1c1; margin-top:10px; text-align:center">height &amp; width must be same, must completely divide 512, and shouldn't be large than 512</h2></body></html>
    """    
            
            #creating dynamic page (404 Error)
            else:
                message = """\
    HTTP/1.1 404 Not Found

    <html><head><title>Error - CN Project</title><link rel="icon" href="data:;base64,iVBORw0KGgo="></head><body><h1 style="font-family:arial; font-size:45px; color:#191919; margin-top:200px; text-align:center">404 Error!</h1><h2 style="font-family:arial; font-size:20px; color:#c1c1c1; margin-top:10px; text-align:center">your requested page doesn\'t exist on this server</h2></body></html>
    """
            
            #sending dynamic html pages
            client_connection.sendall(message)

            #closing socket
            client_connection.close()

        #conditional branching to prevent termination on no request    
        else:
            print "No request recieved!"  


#switching threads      
def switch_thread(delay):

        #putting thread to sleep    
        time.sleep(delay)

        #calling server function
        server_data(1)

#multi threading
try:
   thread.start_new_thread(switch_thread(2))
   thread.start_new_thread(switch_thread(4))
   thread.start_new_thread(switch_thread(2))
   thread.start_new_thread(switch_thread(4))
   thread.start_new_thread(switch_thread(2))
except:
   print "Error: unable to start thread"

