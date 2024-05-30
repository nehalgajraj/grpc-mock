import grpc

# Import the generated client stubs
import ping_service_pb2
import ping_service_pb2_grpc

def run():
    # Channel to connect to serverX
    with grpc.insecure_channel('localhost:50050') as channel:
        stub = ping_service_pb2_grpc.PingServiceStub(channel)
        # Create a PingAARequest and send it
        response = stub.Ping(ping_service_pb2.PingRequest(message="Hello from Client"))
        print("Client received response:", response.message)

if __name__ == '__main__':
    run()
