import grpc
from concurrent import futures
import time

# Import the generated classes
import ping_service_pb2
import ping_service_pb2_grpc
import serverx_to_server_y_pb2
import serverx_to_server_y_pb2_grpc

# Constants for the service
SERVER_Y_GRPC_ADDRESS = 'localhost:50051'
GRPC_PORT = 50050

# gRPC server setup for communicating with serverY
class ServerXPingService(ping_service_pb2_grpc.PingServiceServicer):
    def Ping(self, request, context):
        # Connect to serverY and send the ping request for further processing
        print("XXX1")
        with grpc.insecure_channel(SERVER_Y_GRPC_ADDRESS) as channel:
            print("XXX2")
            stub = serverx_to_server_y_pb2_grpc.ServerYServiceStub(channel)
            print("XXX3")
            # Assume the method to call on serverY is ProcessPing which expects a PingABRequest and returns a PingABResponse
            response = stub.ProcessPing(serverx_to_server_y_pb2.PingABRequest(message=request.message))
            print("XXX4")
            return ping_service_pb2.PingResponse(message=f"Processed on serverX and serverY: {response.message}")

def serve():
    # Create a gRPC server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    ping_service_pb2_grpc.add_PingServiceServicer_to_server(ServerXPingService(), server)
    server.add_insecure_port(f'[::]:{GRPC_PORT}')
    print(f"ServerX running on port {GRPC_PORT}")
    server.start()
    try:
        while True:
            time.sleep(86400)  # Server is kept alive for one day; you can adjust this as needed
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
