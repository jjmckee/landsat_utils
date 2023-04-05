# simple mean
Red_out= 0.5 * (Red_in + Pan_in)
Green_out = 0.5 * (Green_in + Pan_in)
Blue_out= 0.5 * (Blue_in + Pan_in)

# Brovey transformation
Red_out = Red_in / [(blue_in + green_in + red_in) * Pan]

# adjusted Brovey
DNF = (P - IW * I) / (RW * R + GW * G + BW * B)
Red_out = R * DNF
Green_out = G * DNF
Blue_out = B * DNF
Infrared_out = I * DNF

P = panchromatic image
R = red band
G = green band
B = blue band
I = near infrared
W = weight

# intensity, hue, and saturation
Intensity = P - I * IW

# Gram-Schmidt