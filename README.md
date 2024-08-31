# Encrypted Authentication Service

The main goal of this system will be to enable server to server authentication requests which will be
end to end encrypted and will store the data in db using symmetric encryption so that even if anyone
has access to the database, they will not be able to tamper with the data easily.

## Initial targets
The initial target for this project is to provide the following mechanisms

 1. ### End to end encryption middleware
 This middleware will wrap around all other middleware and request/response functions and will decrypt request bodies before any further processing and encrypt response bodies before sending them out.

 2. ### Complete audit trail of requests
 This  middleware will provide complete invasive audit trail of the originating request and the outgoing response and will stream the log generated to a distributed log network to prevent damage to the audit log in case of hardware failure.

 3. ### Encrypted data storage model and db field
 This will provide an easily implementable model base class which will take a set of encrypted data and will decrypt on demand when the model is evaluated and encrypt data on demand when model is serialized.