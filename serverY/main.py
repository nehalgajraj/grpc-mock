import grpc
from concurrent import futures
import time

# Import the generated classes
import serverx_to_server_y_pb2
import serverx_to_server_y_pb2_grpc

# Constants for the service
GRPC_PORT = 50051

# gRPC server setup for processing requests from serverX
class ServerYService(serverx_to_server_y_pb2_grpc.ServerYServiceServicer):
    def ProcessPing(self, request, context):
        print("YYY1")
        # Here we perform some simple logic; in this case, we just append a string
        processed_message = f"{request.message} - processed by serverY"
        print("YYY2")
        return serverx_to_server_y_pb2.PingABResponse(message=processed_message)

def serve():
    # Create a gRPC server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    serverx_to_server_y_pb2_grpc.add_ServerYServiceServicer_to_server(ServerYService(), server)
    server.add_insecure_port(f'[::]:{GRPC_PORT}')
    print(f"ServerY running on port {GRPC_PORT}")
    server.start()
    try:
        while True:
            time.sleep(86400)  # Server is kept alive for one day; you can adjust this as needed
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
