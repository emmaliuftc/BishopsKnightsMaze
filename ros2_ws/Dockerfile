FROM ros:humble-perception

RUN apt-get update && apt-get install -y \
        python3-pip \
	python3-dev \
        i2c-tools \
        libgpiod-dev \
        usbutils \
	gpiod \
        && rm -rf /var/lib/apt/lists/*

WORKDIR /root/ros2_ws

RUN pip3 install --upgrade pip
# RUN pip3 install "setuptools<66" --break-system-packages

COPY requirements.txt .

RUN pip3 install -r requirements.txt --break-system-packages
RUN pip3 install "setuptools<66"
RUN pip3 install dynamixel_sdk
COPY ./src ./src

RUN echo "source /opt/ros/humble/setup.bash" >> /.bashrc
ENV GPIOZERO_PIN_FACTORY=lgpio

# RUN pip3 install "setuptools<66" --break-system-packages
CMD ["bash"]

# RUN pip3 install "setuptools<66" --break-system-packages --root-user-action
