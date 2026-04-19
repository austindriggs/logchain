# WARNING

The hardware section isn't fully implemented yet.

This could be added to the main docker-compose.yml file to be tested:
```yaml
   pico-reader:
      build: .
      container_name: pico-log-reader
      command: python demo/hardware/pico_reader.py
      devices:
        - "/dev/ttyACM0:/dev/ttyACM0"
      privileged: true
      restart: always
```
