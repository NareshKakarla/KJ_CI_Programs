from PIL import Image, ImageDraw, ImageFont
import math

def create_concentric_circles(draw, center, radii, color):
    for radius in radii:
        bbox = [center[0]-radius, center[1]-radius, center[0]+radius, center[1]+radius]
        draw.ellipse(bbox, outline=color)

# Create a new image with a white background
width, height = 800, 600
image = Image.new('RGB', (width, height), color='white')
draw = ImageDraw.Draw(image)

# Draw grid lines
for i in range(0, width, 50):
    draw.line([(i, 0), (i, height)], fill='lightgray')
for i in range(0, height, 50):
    draw.line([(0, i), (width, i)], fill='lightgray')

# Draw LoRa gateways (concentric circles)
gateways = [(300, 200), (300, 400), (500, 300)]
for center in gateways:
    create_concentric_circles(draw, center, [30, 60, 90], 'blue')

# Draw SF nodes
sf_nodes = [(100, 150, "SF7"), (100, 350, "SF8"), (100, 550, "SF10")]
for x, y, label in sf_nodes:
    draw.ellipse([x-20, y-20, x+20, y+20], fill='red')
    draw.text((x-15, y-10), label, fill='white')

# Draw connections
for node in sf_nodes:
    for gateway in gateways:
        draw.line([(node[0], node[1]), gateway], fill='red', width=1)

# Draw Network Server
draw.rectangle([650, 250, 700, 300], fill='gray')
draw.text((655, 305), "Network\nServer", fill='black')

# Draw Internet cloud
cloud_points = [(720, 200), (780, 200), (800, 250), (780, 300), (720, 300), (700, 250)]
draw.polygon(cloud_points, outline='black')
draw.text((730, 240), "Internet", fill='black')

# Add labels
font = ImageFont.load_default()
draw.text((50, 580), "Perceptual Layer", font=font, fill='black')
draw.text((300, 580), "LoRaWAN", font=font, fill='black')
draw.text((650, 580), "Application Layer", font=font, fill='black')

# Save the image
image.save('lora_network_diagram.png')
image.show()