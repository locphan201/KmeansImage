import pygame, random, math, numpy
from sklearn.cluster import KMeans
from color import *

current_K = 0
running = True
points = []
labels = []
clusters = []
error = 0

def calculate_distance(p, c):
    return math.sqrt((p[0] - c[0])**2 + (p[1] - c[1])**2)

def compare_distance(p):
    distance = []
    for c in clusters:
        distance.append(calculate_distance(p, c))
    return distance.index(min(distance))

def new_pos_cluster(labels):
    new_pos = []
    for i in range(current_K):
        new_pos.append([0, 0, 0])

    for label in labels:
        new_pos[label[2]][0] += label[0]
        new_pos[label[2]][1] += label[1]
        new_pos[label[2]][2] += 1
    
    for pos in new_pos:
        if pos[2] != 0:
            pos[0] /= pos[2]
            pos[1] /= pos[2]  
    return new_pos
    
pygame.init()
screen = pygame.display.set_mode((1200, 600))

font = pygame.font.SysFont("sans", 40)
small_font = pygame.font.SysFont("sans", 15)
clock = pygame.time.Clock()

while running:
    screen.fill(BACKGROUND)
    clock.tick(60)
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Draw UI  
    # Draw a panel
    pygame.draw.rect(screen, BLACK, (50, 50, 700, 500))
    pygame.draw.rect(screen, BACKGROUND_PANEL, (55, 55, 690, 490))
    
    # Draw points
    for point in points:
        pygame.draw.circle(screen, BLACK, (point[0] + 50, point[1] + 50), 5)
        pygame.draw.circle(screen, WHITE, (point[0] + 50, point[1] + 50), 4)
    
    # Draw clusters
    for i in range(len(clusters)):
        pygame.draw.circle(screen, color[i], (clusters[i][0] + 50, clusters[i][1] + 50), 5)
    
    # Draw labels
    for label in labels:
        pygame.draw.circle(screen, color[label[2]], (label[0] + 50, label[1] + 50), 4)
    
    # K + button
    pygame.draw.rect(screen, BLACK, (850, 50, 50, 50))
    screen.blit(font.render("+", True, WHITE), (866, 50))
    
    # K - button
    pygame.draw.rect(screen, BLACK, (950, 50, 50, 50))
    screen.blit(font.render("-", True, WHITE), (970, 48))
    
    # Show current K
    screen.blit(font.render("K = " + str(current_K), True, BLACK), (1050, 50))
    
    # Run button
    pygame.draw.rect(screen, BLACK, (850, 150, 150, 50))
    screen.blit(font.render("Run", True, WHITE), (895, 150))
    
    # Random button
    pygame.draw.rect(screen, BLACK, (850, 250, 150, 50))
    screen.blit(font.render("Random", True, WHITE), (865, 250))
    
    # Algorithm button
    pygame.draw.rect(screen, BLACK, (850, 350, 150, 50))
    screen.blit(font.render("Algorithm", True, WHITE), (855, 350))
    
    # Reset button
    pygame.draw.rect(screen, BLACK, (850, 450, 150, 50))
    screen.blit(font.render("Reset", True, WHITE), (880, 450))
    
    # Error show
    screen.blit(font.render('Error: ' + str(int(error)), True, BLACK), (850, 525))
    
    # Cursor position
    if 50 <= mouse_x <= 750 and 50 <= mouse_y <= 550:
        screen.blit(small_font.render("(" + str(mouse_x - 50) + ", " + str(mouse_y - 50) + ")", True, BLACK), (mouse_x + 12, mouse_y + 12))
    # End of UI

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Panel
            if 50 <= mouse_x <= 750 and 50 <= mouse_y <= 550:
                points.append((mouse_x - 50, mouse_y - 50))
            
            # K + button
            if 850 <= mouse_x <= 900 and 50 <= mouse_y <= 100:
                if current_K < 8:
                    current_K += 1
            
            # K - button
            if 950 <= mouse_x <= 1000 and 50 <= mouse_y <= 100:
                if current_K > 0:
                    current_K -= 1
              
            # Run button  
            if 850 <= mouse_x <= 1000 and 150 <= mouse_y <= 200:
                if current_K == 0:
                    continue
                newLabels = []
                for point in points:
                    newLabels.append([point[0], point[1], compare_distance(point)])
                labels = newLabels
                cluster = new_pos_cluster(labels)
                error = 0
                for c in clusters:
                    for l in labels:
                        error += int(calculate_distance(l, c))          
                              
            # Random button
            if 850 <= mouse_x <= 1000 and 250 <= mouse_y <= 300:
                if current_K == 0:
                    continue
                
                newclusters = []
                for i in range(current_K):
                    point = [random.randint(0, 650), random.randint(0, 450)]
                    while newclusters.count(point) > 0:
                        point = [random.randint(0, 650), random.randint(0, 450)]
                    newclusters.append(point)
                clusters = newclusters
                
            # Algorithm button
            if 850 <= mouse_x <= 1000 and 350 <= mouse_y <= 400:
                if current_K == 0:
                    continue          
                kmeans = KMeans(n_clusters=current_K).fit(points)
                lebels = kmeans.predict(points)
                clusters = kmeans.cluster_centers_
                
            # Reset button
            if 850 <= mouse_x <= 1000 and 450 <= mouse_y <= 500:
                labels = []
            
    pygame.display.flip()