import sys
import os
import json
import random
import webbrowser
from typing import Dict, List, Tuple, Optional, Set, Any
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QLabel, QPushButton, QFrame, QScrollArea, QGridLayout, 
                            QRadioButton, QButtonGroup, QGroupBox, QSplitter, QMessageBox,
                            QTabWidget, QComboBox, QFileDialog, QToolBar, QAction, QMenu,
                            QSizePolicy, QSpacerItem, QDialog, QTableWidget, QTableWidgetItem,
                            QProgressBar, QLineEdit, QTextEdit, QCheckBox, QSlider, QToolTip)
from PyQt5.QtGui import (QPixmap, QImage, QPainter, QColor, QFont, QIcon, QCursor, QPalette, 
                        QBrush, QLinearGradient, QRadialGradient, QPen, QFontMetrics, 
                        QMouseEvent, QResizeEvent, QKeyEvent, QDesktopServices)
from PyQt5.QtCore import (Qt, QSize, QRect, QUrl, QBuffer, QByteArray, QIODevice, 
                         pyqtSignal, QThread, QTimer, QPropertyAnimation, QEasingCurve,
                         QPoint, QEvent, QObject, QMargins)

# Constantes de estilo
VALORANT_RED = "#FF4655"
VALORANT_BLUE = "#0F1923"
VALORANT_WHITE = "#ECE8E1"
VALORANT_LIGHT_BLUE = "#1F2731"
VALORANT_DARK_RED = "#BD3944"
VALORANT_ACCENT = "#BDBCB7"

# Colores de roles
ROLE_COLORS = {
    "Duelista": "#FF4655",
    "Iniciador": "#5AA9FE",
    "Controlador": "#BDCF32",
    "Centinela": "#31E8BF"
}

# Colores de tiers
TIER_COLORS = {
    "S-Tier": "#FFD700",  # Gold
    "A-Tier": "#00FF00",  # Green
    "B-Tier": "#1E90FF",  # Blue
    "C-Tier": "#FF6347"   # Red-orange
}

class HoverButton(QPushButton):
    """Botón personalizado con efectos de hover"""
    def __init__(self, text="", parent=None, color=VALORANT_RED, hover_color=VALORANT_DARK_RED):
        super().__init__(text, parent)
        self.color = color
        self.hover_color = hover_color
        self.text_color = VALORANT_WHITE
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.color};
                color: {self.text_color};
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
                font-size: 12px;
            }}
            QPushButton:hover {{
                background-color: {self.hover_color};
            }}
            QPushButton:pressed {{
                background-color: {QColor(self.hover_color).darker(120).name()};
            }}
        """)

class AgentCard(QFrame):
    """Widget personalizado para mostrar un agente con su imagen, nombre y tier"""
    clicked = pyqtSignal(str)  # Señal que emite el nombre del agente cuando se hace clic
    info_clicked = pyqtSignal(str)  # Señal que emite el nombre del agente cuando se hace clic en info
    
    def __init__(self, agent_name, role, tier, image=None, parent=None, size_factor=1.0):
        super().__init__(parent)
        self.agent_name = agent_name
        self.role = role
        self.tier = tier
        self.image = image
        self.is_selected = False
        self.is_preferred = False
        self.size_factor = size_factor
        
        # Configuración del estilo
        self.setObjectName("agentCard")
        self.setStyleSheet(f"""
            #agentCard {{
                background-color: {VALORANT_LIGHT_BLUE};
                border-radius: 8px;
                padding: 5px;
                margin: 5px;
            }}
            #agentCard:hover {{
                background-color: #2A3441;
                border: 1px solid {VALORANT_RED};
            }}
        """)
        
        # Configuración del layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(8, 8, 8, 8)
        self.layout.setSpacing(4)
        
        # Imagen del agente
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        img_size = int(80 * self.size_factor)
        self.image_label.setMinimumSize(img_size, img_size)
        self.image_label.setMaximumSize(img_size, img_size)
        self.layout.addWidget(self.image_label)
        
        # Nombre del agente
        self.name_label = QLabel(agent_name)
        self.name_label.setAlignment(Qt.AlignCenter)
        self.name_label.setStyleSheet(f"color: {VALORANT_WHITE}; font-weight: bold; font-size: {10 * self.size_factor}pt;")
        self.layout.addWidget(self.name_label)
        
        # Tier del agente
        self.tier_label = QLabel(tier)
        self.tier_label.setAlignment(Qt.AlignCenter)
        self.set_tier_color()
        self.layout.addWidget(self.tier_label)
        
        # Botón de información
        self.info_button = QPushButton("ℹ️")
        self.info_button.setStyleSheet("""
            background-color: transparent;
            color: white;
            border: none;
            padding: 2px;
            font-size: 12px;
        """)
        self.info_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.info_button.clicked.connect(self.on_info_clicked)
        self.layout.addWidget(self.info_button)
        
        # Establecer la imagen
        self.set_image(image)
        
        # Hacer que el widget sea clickeable
        self.setCursor(QCursor(Qt.PointingHandCursor))
    
    def set_image(self, image):
        """Establecer la imagen del agente"""
        if image:
            self.image = image
            pixmap = QPixmap.fromImage(image)
            img_size = int(80 * self.size_factor)
            pixmap = pixmap.scaled(img_size, img_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.image_label.setPixmap(pixmap)
        else:
            # Crear imagen de placeholder
            self.create_placeholder_image()
    
    def create_placeholder_image(self):
        """Crear una imagen de placeholder con el nombre del agente"""
        # Determinar color según el rol
        color = ROLE_COLORS.get(self.role, VALORANT_WHITE)
        
        # Crear imagen
        img_size = int(80 * self.size_factor)
        image = QImage(img_size, img_size, QImage.Format_ARGB32)
        image.fill(QColor(VALORANT_BLUE))
        
        painter = QPainter(image)
        painter.setPen(QColor(color))
        painter.setBrush(QColor(color).darker(150))
        painter.drawRoundedRect(5, 5, img_size-10, img_size-10, 10, 10)
        
        # Añadir texto
        painter.setPen(QColor(VALORANT_WHITE))
        font_size = int(12 * self.size_factor)
        font = QFont("Arial", font_size, QFont.Bold)
        painter.setFont(font)
        painter.drawText(QRect(5, 5, img_size-10, img_size-10), Qt.AlignCenter, self.agent_name)
        painter.end()
        
        # Establecer la imagen
        self.image_label.setPixmap(QPixmap.fromImage(image))
    
    def set_tier_color(self):
        """Establecer el color del tier"""
        color = TIER_COLORS.get(self.tier, VALORANT_WHITE)
        self.tier_label.setStyleSheet(f"color: {color}; font-size: {8 * self.size_factor}pt;")
    
    def set_selected(self, selected):
        """Marcar el agente como seleccionado"""
        self.is_selected = selected
        if selected:
            self.setStyleSheet(f"""
                #agentCard {{
                    background-color: #2A3441;
                    border: 2px solid {VALORANT_RED};
                    border-radius: 8px;
                    padding: 5px;
                    margin: 5px;
                }}
            """)
        else:
            self.setStyleSheet(f"""
                #agentCard {{
                    background-color: {VALORANT_LIGHT_BLUE};
                    border-radius: 8px;
                    padding: 5px;
                    margin: 5px;
                }}
                #agentCard:hover {{
                    background-color: #2A3441;
                    border: 1px solid {VALORANT_RED};
                }}
            """)
    
    def set_preferred(self, preferred):
        """Marcar el agente como preferido"""
        self.is_preferred = preferred
        if preferred:
            self.name_label.setText(f"{self.agent_name} ★")
        else:
            self.name_label.setText(self.agent_name)
    
    def on_info_clicked(self):
        """Manejar el clic en el botón de información"""
        self.info_clicked.emit(self.agent_name)
    
    def mousePressEvent(self, event):
        """Manejar el evento de clic"""
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self.agent_name)
        super().mousePressEvent(event)
    
    def set_size_factor(self, factor):
        """Actualizar el factor de tamaño y redimensionar elementos"""
        self.size_factor = factor
        
        # Actualizar tamaños
        img_size = int(80 * self.size_factor)
        self.image_label.setMinimumSize(img_size, img_size)
        self.image_label.setMaximumSize(img_size, img_size)
        
        # Actualizar estilos
        self.name_label.setStyleSheet(f"color: {VALORANT_WHITE}; font-weight: bold; font-size: {10 * self.size_factor}pt;")
        self.set_tier_color()
        
        # Actualizar imagen
        if self.image:
            self.set_image(self.image)
        else:
            self.create_placeholder_image()

class MapCard(QFrame):
    """Widget personalizado para mostrar un mapa con su imagen y nombre"""
    clicked = pyqtSignal(str)  # Señal que emite el nombre del mapa cuando se hace clic
    
    def __init__(self, map_name, image=None, parent=None, size_factor=1.0):
        super().__init__(parent)
        self.map_name = map_name
        self.image = image
        self.is_selected = False
        self.size_factor = size_factor
        
        # Configuración del estilo
        self.setObjectName("mapCard")
        self.setStyleSheet(f"""
            #mapCard {{
                background-color: {VALORANT_LIGHT_BLUE};
                border-radius: 8px;
                padding: 5px;
                margin: 2px;
            }}
            #mapCard:hover {{
                background-color: #2A3441;
                border: 1px solid {VALORANT_RED};
            }}
        """)
        
        # Configuración del layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(5, 5, 5, 5)
        self.layout.setSpacing(2)
        
        # Imagen del mapa
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        img_width = int(160 * self.size_factor)
        img_height = int(90 * self.size_factor)
        self.image_label.setMinimumSize(img_width, img_height)
        self.image_label.setMaximumSize(img_width, img_height)
        self.layout.addWidget(self.image_label)
        
        # Nombre del mapa
        self.name_label = QLabel(map_name)
        self.name_label.setAlignment(Qt.AlignCenter)
        self.name_label.setStyleSheet(f"color: {VALORANT_WHITE}; font-weight: bold; font-size: {10 * self.size_factor}pt;")
        self.layout.addWidget(self.name_label)
        
        # Establecer la imagen
        self.set_image(image)
        
        # Hacer que el widget sea clickeable
        self.setCursor(QCursor(Qt.PointingHandCursor))
    
    def set_image(self, image):
        """Establecer la imagen del mapa"""
        if image:
            self.image = image
            pixmap = QPixmap.fromImage(image)
            img_width = int(160 * self.size_factor)
            img_height = int(90 * self.size_factor)
            pixmap = pixmap.scaled(img_width, img_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.image_label.setPixmap(pixmap)
        else:
            # Crear imagen de placeholder
            self.create_placeholder_image()
    
    def create_placeholder_image(self):
        """Crear una imagen de placeholder con el nombre del mapa"""
        # Crear imagen
        img_width = int(160 * self.size_factor)
        img_height = int(90 * self.size_factor)
        image = QImage(img_width, img_height, QImage.Format_ARGB32)
        image.fill(QColor(VALORANT_BLUE))
        
        painter = QPainter(image)
        painter.setPen(QColor(VALORANT_RED))
        painter.setBrush(QColor(VALORANT_LIGHT_BLUE))
        painter.drawRoundedRect(5, 5, img_width-10, img_height-10, 10, 10)
        
        # Añadir texto
        painter.setPen(QColor(VALORANT_WHITE))
        font_size = int(12 * self.size_factor)
        font = QFont("Arial", font_size, QFont.Bold)
        painter.setFont(font)
        painter.drawText(QRect(5, 5, img_width-10, img_height-10), Qt.AlignCenter, self.map_name)
        painter.end()
        
        # Establecer la imagen
        self.image_label.setPixmap(QPixmap.fromImage(image))
    
    def set_selected(self, selected):
        """Marcar el mapa como seleccionado"""
        self.is_selected = selected
        if selected:
            self.setStyleSheet(f"""
                #mapCard {{
                    background-color: #2A3441;
                    border: 2px solid {VALORANT_RED};
                    border-radius: 8px;
                    padding: 5px;
                    margin: 5px;
                }}
            """)
        else:
            self.setStyleSheet(f"""
                #mapCard {{
                    background-color: {VALORANT_LIGHT_BLUE};
                    border-radius: 8px;
                    padding: 5px;
                    margin: 5px;
                }}
                #mapCard:hover {{
                    background-color: #2A3441;
                    border: 1px solid {VALORANT_RED};
                }}
            """)
    
    def mousePressEvent(self, event):
        """Manejar el evento de clic"""
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self.map_name)
        super().mousePressEvent(event)
    
    def set_size_factor(self, factor):
        """Actualizar el factor de tamaño y redimensionar elementos"""
        self.size_factor = factor
        
        # Actualizar tamaños
        img_width = int(160 * self.size_factor)
        img_height = int(90 * self.size_factor)
        self.image_label.setMinimumSize(img_width, img_height)
        self.image_label.setMaximumSize(img_width, img_height)
        
        # Actualizar estilos
        self.name_label.setStyleSheet(f"color: {VALORANT_WHITE}; font-weight: bold; font-size: {10 * self.size_factor}pt;")
        
        # Actualizar imagen
        if self.image:
            self.set_image(self.image)
        else:
            self.create_placeholder_image()

class RoleButton(QPushButton):
    """Botón personalizado para selección de rol"""
    def __init__(self, role, parent=None):
        super().__init__(role, parent)
        self.role = role
        
        # Configurar estilo según el rol
        role_colors = {
            "Todos": "#333333",
            "Duelista": ROLE_COLORS["Duelista"],
            "Iniciador": ROLE_COLORS["Iniciador"],
            "Controlador": ROLE_COLORS["Controlador"],
            "Centinela": ROLE_COLORS["Centinela"]
        }
        
        text_color = 'white' if role in ['Todos', 'Duelista'] else '#0F1923'
        
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {role_colors[role]};
                color: {text_color};
                border: none;
                border-radius: 4px;
                padding: 5px 10px;
                font-weight: bold;
                font-size: 10px;
            }}
            QPushButton:hover {{
                background-color: {QColor(role_colors[role]).lighter(110).name()};
            }}
            QPushButton:pressed {{
                background-color: {QColor(role_colors[role]).darker(110).name()};
            }}
        """)
        
        self.setCursor(QCursor(Qt.PointingHandCursor))

class StyleRadioButton(QRadioButton):
    """Botón de radio personalizado para estilos de juego"""
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet(f"""
            QRadioButton {{
                color: {VALORANT_WHITE};
                font-size: 12px;
                spacing: 8px;
            }}
            QRadioButton::indicator {{
                width: 16px;
                height: 16px;
                border-radius: 8px;
            }}
            QRadioButton::indicator:unchecked {{
                border: 2px solid {VALORANT_WHITE};
                background-color: transparent;
            }}
            QRadioButton::indicator:checked {{
                border: 2px solid {VALORANT_RED};
                background-color: {VALORANT_RED};
            }}
        """)

class AnimatedProgressBar(QProgressBar):
    """Barra de progreso animada personalizada"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setRange(0, 100)
        self.setValue(0)
        self.setTextVisible(False)
        self.setStyleSheet(f"""
            QProgressBar {{
                border: none;
                border-radius: 4px;
                background-color: {VALORANT_LIGHT_BLUE};
                height: 8px;
            }}
            QProgressBar::chunk {{
                background-color: {VALORANT_RED};
                border-radius: 4px;
            }}
        """)
        
        # Animación
        self.animation_timer = QTimer(self)
        self.animation_timer.timeout.connect(self.update_animation)
        self.animation_value = 0
        
    def start_animation(self):
        """Iniciar animación"""
        self.animation_value = 0
        self.setValue(0)
        self.animation_timer.start(20)
        
    def update_animation(self):
        """Actualizar valor de la animación"""
        self.animation_value += 2
        if self.animation_value > 100:
            self.animation_timer.stop()
            self.animation_value = 100
        self.setValue(self.animation_value)

class AgentInfoDialog(QDialog):
    """Diálogo para mostrar información detallada de un agente"""
    def __init__(self, agent_name, agent_data, agent_image=None, parent=None):
        super().__init__(parent)
        self.agent_name = agent_name
        self.agent_data = agent_data
        self.agent_image = agent_image
        
        self.setWindowTitle(f"Información de {agent_name}")
        self.setMinimumSize(600, 700)
        self.setStyleSheet(f"""
            QDialog {{
                background-color: {VALORANT_BLUE};
            }}
            QLabel {{
                color: {VALORANT_WHITE};
                font-family: "Segoe UI", sans-serif;
            }}
            QTabWidget::pane {{
                border: 1px solid #2A3441;
                background-color: {VALORANT_LIGHT_BLUE};
                border-radius: 8px;
            }}
            QTabBar::tab {{
                background-color: {VALORANT_LIGHT_BLUE};
                color: {VALORANT_WHITE};
                border: 1px solid #2A3441;
                border-bottom: none;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                padding: 8px 12px;
                margin-right: 2px;
            }}
            QTabBar::tab:selected {{
                background-color: {VALORANT_RED};
                color: white;
            }}
            QTabBar::tab:!selected {{
                margin-top: 2px;
            }}
        """)
        
        # Layout principal
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Cabecera con imagen y datos básicos
        self.create_header(layout)
        
        # Tabs para organizar la información
        tab_widget = QTabWidget()
        layout.addWidget(tab_widget)
        
        # Tab de habilidades
        abilities_tab = QWidget()
        self.create_abilities_tab(abilities_tab)
        tab_widget.addTab(abilities_tab, "Habilidades")
        
        # Tab de estrategias
        strategies_tab = QWidget()
        self.create_strategies_tab(strategies_tab)
        tab_widget.addTab(strategies_tab, "Estrategias")
        
        # Tab de estadísticas
        stats_tab = QWidget()
        self.create_stats_tab(stats_tab)
        tab_widget.addTab(stats_tab, "Estadísticas")
        
        # Tab de lineups
        lineups_tab = QWidget()
        self.create_lineups_tab(lineups_tab)
        tab_widget.addTab(lineups_tab, "Lineups")
        
        # Botones de acción
        button_layout = QHBoxLayout()
        
        # Botón para ver guías oficiales
        guides_button = HoverButton("Ver Guías Oficiales", color="#1F2731")
        guides_button.clicked.connect(self.open_official_guides)
        button_layout.addWidget(guides_button)
        
        # Botón para ver videos
        videos_button = HoverButton("Ver Videos", color="#1F2731")
        videos_button.clicked.connect(self.open_videos)
        button_layout.addWidget(videos_button)
        
        # Botón para cerrar
        close_button = HoverButton("Cerrar")
        close_button.clicked.connect(self.accept)
        button_layout.addWidget(close_button)
        
        layout.addLayout(button_layout)
    
    def create_header(self, layout):
        """Crear cabecera con imagen y datos básicos del agente"""
        header_frame = QFrame()
        header_frame.setStyleSheet(f"background-color: {VALORANT_LIGHT_BLUE}; border-radius: 8px;")
        header_layout = QHBoxLayout(header_frame)
        
        # Imagen del agente
        image_frame = QFrame()
        image_layout = QVBoxLayout(image_frame)
        
        image_label = QLabel()
        if self.agent_image:
            pixmap = QPixmap.fromImage(self.agent_image)
            pixmap = pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            image_label.setPixmap(pixmap)
        else:
            # Crear imagen de placeholder
            self.create_placeholder_image(image_label)
        
        image_label.setAlignment(Qt.AlignCenter)
        image_layout.addWidget(image_label)
        
        # Tier del agente
        tier = self.get_agent_tier()
        tier_color = TIER_COLORS.get(tier, VALORANT_WHITE)
        
        tier_label = QLabel(f"{tier}")
        tier_label.setStyleSheet(f"color: {tier_color}; font-size: 14px; font-weight: bold;")
        tier_label.setAlignment(Qt.AlignCenter)
        image_layout.addWidget(tier_label)
        
        header_layout.addWidget(image_frame)
        
        # Información básica
        info_frame = QFrame()
        info_layout = QVBoxLayout(info_frame)
        
        # Nombre del agente
        name_label = QLabel(self.agent_name)
        name_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        info_layout.addWidget(name_label)
        
        # Rol
        role = self.get_agent_role()
        role_color = ROLE_COLORS.get(role, VALORANT_WHITE)
        
        role_label = QLabel(role)
        role_label.setStyleSheet(f"font-size: 18px; color: {role_color};")
        info_layout.addWidget(role_label)
        
        # Datos adicionales
        if "real_name" in self.agent_data:
            info_label = QLabel(f"Nombre real: {self.agent_data['real_name']}")
            info_label.setStyleSheet("font-size: 14px;")
            info_layout.addWidget(info_label)
        
        if "origin" in self.agent_data:
            info_label = QLabel(f"Origen: {self.agent_data['origin']}")
            info_label.setStyleSheet("font-size: 14px;")
            info_layout.addWidget(info_label)
        
        if "playstyle" in self.agent_data:
            info_label = QLabel(f"Estilo de juego: {self.agent_data['playstyle']}")
            info_label.setStyleSheet("font-size: 14px;")
            info_layout.addWidget(info_label)
        
        # Descripción
        if "description" in self.agent_data:
            desc_label = QLabel(self.agent_data["description"])
            desc_label.setStyleSheet("font-size: 12px; font-style: italic;")
            desc_label.setWordWrap(True)
            info_layout.addWidget(desc_label)
        
        header_layout.addWidget(info_frame, 1)  # 1 = stretch factor
        
        layout.addWidget(header_frame)
    
    def create_abilities_tab(self, tab):
        """Crear tab de habilidades"""
        layout = QVBoxLayout(tab)
        
        if "abilities" in self.agent_data:
            abilities = self.agent_data["abilities"]
            
            for i, ability in enumerate(abilities):
                ability_frame = QFrame()
                ability_frame.setStyleSheet(f"background-color: {VALORANT_LIGHT_BLUE}; border-radius: 8px;")
                ability_layout = QVBoxLayout(ability_frame)
                
                # Nombre de la habilidad
                ability_name = QLabel(ability)
                ability_name.setStyleSheet(f"font-size: 16px; font-weight: bold; color: {VALORANT_RED};")
                ability_layout.addWidget(ability_name)
                
                # Descripción de la habilidad (simulada)
                ability_desc = QLabel(f"Descripción de {ability}. Esta es una descripción simulada de la habilidad.")
                ability_desc.setWordWrap(True)
                ability_desc.setStyleSheet("font-size: 12px;")
                ability_layout.addWidget(ability_desc)
                
                # Consejos de uso
                tips_label = QLabel("Consejos de uso:")
                tips_label.setStyleSheet("font-size: 12px; font-weight: bold;")
                ability_layout.addWidget(tips_label)
                
                tips = QLabel("• Utiliza esta habilidad estratégicamente para maximizar su efectividad.\n• Coordina con tu equipo para combinar habilidades.")
                tips.setWordWrap(True)
                tips.setWordWrap(True)
                tips.setStyleSheet("font-size: 12px;")
                ability_layout.addWidget(tips)
                
                layout.addWidget(ability_frame)
        else:
            # Mensaje de información no disponible
            no_info_label = QLabel("Información de habilidades no disponible para este agente.")
            no_info_label.setStyleSheet("font-size: 14px; font-style: italic;")
            no_info_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(no_info_label)
        
        # Añadir espaciador para alinear al principio
        layout.addStretch()
    
    def create_strategies_tab(self, tab):
        """Crear tab de estrategias"""
        layout = QVBoxLayout(tab)
        
        # Estrategias ofensivas
        offensive_frame = QFrame()
        offensive_frame.setStyleSheet(f"background-color: {VALORANT_LIGHT_BLUE}; border-radius: 8px;")
        offensive_layout = QVBoxLayout(offensive_frame)
        
        offensive_title = QLabel("Estrategias Ofensivas")
        offensive_title.setStyleSheet(f"font-size: 16px; font-weight: bold; color: {VALORANT_RED};")
        offensive_layout.addWidget(offensive_title)
        
        offensive_tips = QLabel("""
• Utiliza las habilidades de movilidad para tomar ángulos inesperados.
• Coordina con iniciadores para entrar después de sus flashes o información.
• Comunica claramente tus intenciones al equipo antes de ejecutar jugadas agresivas.
• Aprende los timings de cada mapa para sorprender a los defensores.
        """)
        offensive_tips.setWordWrap(True)
        offensive_tips.setStyleSheet("font-size: 12px;")
        offensive_layout.addWidget(offensive_tips)
        
        layout.addWidget(offensive_frame)
        
        # Estrategias defensivas
        defensive_frame = QFrame()
        defensive_frame.setStyleSheet(f"background-color: {VALORANT_LIGHT_BLUE}; border-radius: 8px;")
        defensive_layout = QVBoxLayout(defensive_frame)
        
        defensive_title = QLabel("Estrategias Defensivas")
        defensive_title.setStyleSheet(f"font-size: 16px; font-weight: bold; color: {VALORANT_RED};")
        defensive_layout.addWidget(defensive_title)
        
        defensive_tips = QLabel("""
• Posiciónate en ángulos no convencionales para sorprender a los atacantes.
• Utiliza tu utilidad para retrasar pushes y ganar tiempo para rotaciones.
• No uses toda tu utilidad al principio de la ronda.
• Comunica información sobre el número de enemigos y su utilidad usada.
        """)
        defensive_tips.setWordWrap(True)
        defensive_tips.setStyleSheet("font-size: 12px;")
        defensive_layout.addWidget(defensive_tips)
        
        layout.addWidget(defensive_frame)
        
        # Mapas recomendados
        maps_frame = QFrame()
        maps_frame.setStyleSheet(f"background-color: {VALORANT_LIGHT_BLUE}; border-radius: 8px;")
        maps_layout = QVBoxLayout(maps_frame)
        
        maps_title = QLabel("Mapas Recomendados")
        maps_title.setStyleSheet(f"font-size: 16px; font-weight: bold; color: {VALORANT_RED};")
        maps_layout.addWidget(maps_title)
        
        # Generar mapas recomendados según el agente
        recommended_maps = self.get_recommended_maps()
        
        maps_text = "• " + "\n• ".join(recommended_maps)
        maps_label = QLabel(maps_text)
        maps_label.setWordWrap(True)
        maps_label.setStyleSheet("font-size: 12px;")
        maps_layout.addWidget(maps_label)
        
        layout.addWidget(maps_frame)
        
        # Añadir espaciador para alinear al principio
        layout.addStretch()
    
    def create_stats_tab(self, tab):
        """Crear tab de estadísticas"""
        layout = QVBoxLayout(tab)
        
        # Estadísticas generales
        stats_frame = QFrame()
        stats_frame.setStyleSheet(f"background-color: {VALORANT_LIGHT_BLUE}; border-radius: 8px;")
        stats_layout = QVBoxLayout(stats_frame)
        
        stats_title = QLabel("Estadísticas de Rendimiento")
        stats_title.setStyleSheet(f"font-size: 16px; font-weight: bold; color: {VALORANT_RED};")
        stats_layout.addWidget(stats_title)
        
        # Generar estadísticas simuladas
        stats = self.generate_simulated_stats()
        
        # Mostrar estadísticas con barras de progreso
        for stat_name, stat_value in stats.items():
            stat_frame = QFrame()
            stat_layout = QHBoxLayout(stat_frame)
            stat_layout.setContentsMargins(0, 0, 0, 0)
            
            stat_label = QLabel(f"{stat_name}:")
            stat_label.setMinimumWidth(150)
            stat_layout.addWidget(stat_label)
            
            progress = QProgressBar()
            progress.setRange(0, 100)
            progress.setValue(stat_value)
            progress.setTextVisible(True)
            progress.setFormat(f"{stat_value}%")
            progress.setStyleSheet(f"""
                QProgressBar {{
                    border: none;
                    border-radius: 4px;
                    background-color: {VALORANT_BLUE};
                    text-align: center;
                    height: 20px;
                }}
                QProgressBar::chunk {{
                    background-color: {VALORANT_RED};
                    border-radius: 4px;
                }}
            """)
            stat_layout.addWidget(progress)
            
            stats_layout.addWidget(stat_frame)
        
        layout.addWidget(stats_frame)
        
        # Popularidad por rango
        rank_frame = QFrame()
        rank_frame.setStyleSheet(f"background-color: {VALORANT_LIGHT_BLUE}; border-radius: 8px;")
        rank_layout = QVBoxLayout(rank_frame)
        
        rank_title = QLabel("Popularidad por Rango")
        rank_title.setStyleSheet(f"font-size: 16px; font-weight: bold; color: {VALORANT_RED};")
        rank_layout.addWidget(rank_title)
        
        # Generar popularidad simulada por rango
        ranks = self.generate_simulated_rank_popularity()
        
        # Mostrar popularidad por rango con barras de progreso
        for rank_name, rank_value in ranks.items():
            rank_frame = QFrame()
            rank_layout = QHBoxLayout(rank_frame)
            rank_layout.setContentsMargins(0, 0, 0, 0)
            
            rank_label = QLabel(f"{rank_name}:")
            rank_label.setMinimumWidth(150)
            rank_layout.addWidget(rank_label)
            
            progress = QProgressBar()
            progress.setRange(0, 100)
            progress.setValue(rank_value)
            progress.setTextVisible(True)
            progress.setFormat(f"{rank_value}%")
            progress.setStyleSheet(f"""
                QProgressBar {{
                    border: none;
                    border-radius: 4px;
                    background-color: {VALORANT_BLUE};
                    text-align: center;
                    height: 20px;
                }}
                QProgressBar::chunk {{
                    background-color: {VALORANT_RED};
                    border-radius: 4px;
                }}
            """)
            rank_layout.addWidget(progress)
            
            rank_layout.addWidget(rank_frame)
        
        layout.addWidget(rank_frame)
        
        # Añadir espaciador para alinear al principio
        layout.addStretch()
    
    def create_lineups_tab(self, tab):
        """Crear tab de lineups"""
        layout = QVBoxLayout(tab)
        
        # Mensaje de lineups
        lineups_frame = QFrame()
        lineups_frame.setStyleSheet(f"background-color: {VALORANT_LIGHT_BLUE}; border-radius: 8px;")
        lineups_layout = QVBoxLayout(lineups_frame)
        
        lineups_title = QLabel("Lineups Populares")
        lineups_title.setStyleSheet(f"font-size: 16px; font-weight: bold; color: {VALORANT_RED};")
        lineups_layout.addWidget(lineups_title)
        
        # Mensaje de lineups
        lineups_msg = QLabel("Los lineups son posiciones específicas donde puedes lanzar habilidades para afectar áreas estratégicas del mapa.")
        lineups_msg.setWordWrap(True)
        lineups_msg.setStyleSheet("font-size: 12px;")
        lineups_layout.addWidget(lineups_msg)
        
        # Botón para ver lineups en YouTube
        youtube_button = HoverButton("Ver Lineups en YouTube", color="#1F2731")
        youtube_button.clicked.connect(self.open_youtube_lineups)
        lineups_layout.addWidget(youtube_button)
        
        layout.addWidget(lineups_frame)
        
        # Lineups por mapa (simulados)
        maps = ["Ascent", "Bind", "Haven", "Split", "Icebox"]
        
        for map_name in maps:
            map_frame = QFrame()
            map_frame.setStyleSheet(f"background-color: {VALORANT_LIGHT_BLUE}; border-radius: 8px;")
            map_layout = QVBoxLayout(map_frame)
            
            map_title = QLabel(f"Lineups en {map_name}")
            map_title.setStyleSheet(f"font-size: 14px; font-weight: bold; color: {VALORANT_RED};")
            map_layout.addWidget(map_title)
            
            # Descripción de lineups para este mapa
            map_desc = QLabel(f"Lineups específicos para {map_name} con {self.agent_name}.")
            map_desc.setWordWrap(True)
            map_desc.setStyleSheet("font-size: 12px;")
            map_layout.addWidget(map_desc)
            
            # Sitios
            sites = ["Sitio A", "Sitio B"]
            if map_name == "Haven":
                sites.append("Sitio C")
            
            for site in sites:
                site_label = QLabel(f"• {site}: Posición para post-planta / retake")
                site_label.setStyleSheet("font-size: 12px;")
                map_layout.addWidget(site_label)
            
            layout.addWidget(map_frame)
        
        # Añadir espaciador para alinear al principio
        layout.addStretch()
    
    def create_placeholder_image(self, label):
        """Crear imagen de placeholder para el agente"""
        role = self.get_agent_role()
        color = ROLE_COLORS.get(role, VALORANT_WHITE)
        
        # Crear imagen
        image = QImage(150, 150, QImage.Format_ARGB32)
        image.fill(QColor(VALORANT_BLUE))
        
        painter = QPainter(image)
        painter.setPen(QColor(color))
        painter.setBrush(QColor(color).darker(150))
        painter.drawRoundedRect(10, 10, 130, 130, 15, 15)
        
        # Añadir texto
        painter.setPen(QColor(VALORANT_WHITE))
        font = QFont("Arial", 20, QFont.Bold)
        painter.setFont(font)
        painter.drawText(QRect(10, 10, 130, 130), Qt.AlignCenter, self.agent_name)
        painter.end()
        
        # Establecer la imagen
        label.setPixmap(QPixmap.fromImage(image))
    
    def get_agent_role(self):
        """Obtener el rol del agente desde los datos o simularlo"""
        if "role" in self.agent_data:
            return self.agent_data["role"]
        
        # Simular rol basado en el nombre del agente
        agent_roles = {
            "Jett": "Duelista",
            "Raze": "Duelista",
            "Phoenix": "Duelista",
            "Reyna": "Duelista",
            "Neon": "Duelista",
            "Yoru": "Duelista",
            "Iso": "Duelista",
            "Sova": "Iniciador",
            "Breach": "Iniciador",
            "Skye": "Iniciador",
            "KAY/O": "Iniciador",
            "Fade": "Iniciador",
            "Gekko": "Iniciador",
            "Tejo": "Iniciador",
            "Waylay": "Iniciador",
            "Brimstone": "Controlador",
            "Viper": "Controlador",
            "Omen": "Controlador",
            "Astra": "Controlador",
            "Harbor": "Controlador",
            "Clove": "Controlador",
            "Killjoy": "Centinela",
            "Cypher": "Centinela",
            "Sage": "Centinela",
            "Chamber": "Centinela",
            "Deadlock": "Centinela",
            "Vyse": "Centinela"
        }
        
        return agent_roles.get(self.agent_name, "Desconocido")
    
    def get_agent_tier(self):
        """Obtener el tier del agente desde los datos o simularlo"""
        if "tier" in self.agent_data:
            return self.agent_data["tier"]
        
        # Simular tier basado en el nombre del agente
        agent_tiers = {
            "Tejo": "S-Tier",
            "Clove": "S-Tier",
            "Raze": "S-Tier",
            "Vyse": "S-Tier",
            "Yoru": "A-Tier",
            "Deadlock": "A-Tier",
            "Cypher": "A-Tier",
            "Jett": "A-Tier",
            "Iso": "A-Tier",
            "Neon": "A-Tier",
            "Sova": "A-Tier",
            "Gekko": "A-Tier",
            "Killjoy": "A-Tier",
            "Omen": "A-Tier",
            "Brimstone": "A-Tier",
            "Phoenix": "A-Tier",
            "Sage": "A-Tier",
            "Chamber": "B-Tier",
            "Viper": "B-Tier",
            "Breach": "B-Tier",
            "Skye": "B-Tier",
            "Fade": "B-Tier",
            "Astra": "B-Tier",
            "Reyna": "B-Tier",
            "Waylay": "C-Tier",
            "KAY/O": "C-Tier",
            "Harbor": "C-Tier"
        }
        
        return agent_tiers.get(self.agent_name, "No clasificado")
    
    def get_recommended_maps(self):
        """Obtener mapas recomendados para el agente"""
        role = self.get_agent_role()
        
        # Mapas recomendados según el rol
        if role == "Duelista":
            return ["Ascent - Excelente para operaciones agresivas y flanqueos",
                   "Split - Ideal para movimiento vertical y control de espacios cerrados",
                   "Fracture - Bueno para entradas rápidas desde múltiples ángulos"]
        elif role == "Iniciador":
            return ["Haven - Perfecto para recopilar información en los tres sitios",
                   "Breeze - Ideal para reconocimiento en espacios abiertos",
                   "Lotus - Bueno para detectar enemigos a través de las puertas rotatorias"]
        elif role == "Controlador":
            return ["Icebox - Esencial para dividir sitios con humos",
                   "Pearl - Ideal para control de líneas de visión largas",
                   "Bind - Perfecto para controlar áreas clave con humos"]
        elif role == "Centinela":
            return ["Bind - Excelente para controlar flancos en los teletransportadores",
                   "Ascent - Ideal para defender sitios y controlar mid",
                   "Fracture - Perfecto para vigilar múltiples entradas"]
        else:
            return ["Información no disponible para este agente"]
    
    def generate_simulated_stats(self):
        """Generar estadísticas simuladas para el agente"""
        import random
        
        # Estadísticas base según el rol
        role = self.get_agent_role()
        tier = self.get_agent_tier()
        
        # Ajustar base según tier
        tier_modifier = {
            "S-Tier": 15,
            "A-Tier": 10,
            "B-Tier": 5,
            "C-Tier": 0,
            "No clasificado": 0
        }
        
        base_modifier = tier_modifier.get(tier, 0)
        
        if role == "Duelista":
            base_stats = {
                "Win Rate": 50 + base_modifier,
                "Pick Rate": 45 + base_modifier,
                "First Blood Rate": 60 + base_modifier,
                "Attack Win Rate": 55 + base_modifier,
                "Defense Win Rate": 45 + base_modifier
            }
        elif role == "Iniciador":
            base_stats = {
                "Win Rate": 52 + base_modifier,
                "Pick Rate": 40 + base_modifier,
                "Assist Rate": 65 + base_modifier,
                "Attack Win Rate": 50 + base_modifier,
                "Defense Win Rate": 50 + base_modifier
            }
        elif role == "Controlador":
            base_stats = {
                "Win Rate": 51 + base_modifier,
                "Pick Rate": 35 + base_modifier,
                "Site Control Rate": 70 + base_modifier,
                "Attack Win Rate": 48 + base_modifier,
                "Defense Win Rate": 52 + base_modifier
            }
        elif role == "Centinela":
            base_stats = {
                "Win Rate": 53 + base_modifier,
                "Pick Rate": 30 + base_modifier,
                "Site Defense Rate": 75 + base_modifier,
                "Attack Win Rate": 45 + base_modifier,
                "Defense Win Rate": 60 + base_modifier
            }
        else:
            base_stats = {
                "Win Rate": 50,
                "Pick Rate": 30,
                "Effectiveness": 50,
                "Attack Win Rate": 50,
                "Defense Win Rate": 50
            }
        
        # Añadir variación aleatoria
        stats = {}
        for stat, value in base_stats.items():
            # Asegurar que el valor esté entre 1 y 99
            random_value = max(1, min(99, value + random.randint(-5, 5)))
            stats[stat] = random_value
        
        return stats
    
    def generate_simulated_rank_popularity(self):
        """Generar popularidad simulada por rango"""
        import random
        
        # Rangos de Valorant
        ranks = ["Hierro", "Bronce", "Plata", "Oro", "Platino", "Diamante", "Ascendente", "Inmortal", "Radiante"]
        
        # Popularidad base según el tier
        tier = self.get_agent_tier()
        
        if tier == "S-Tier":
            base_values = [30, 40, 50, 60, 70, 75, 80, 85, 90]
        elif tier == "A-Tier":
            base_values = [40, 45, 50, 55, 60, 65, 70, 75, 80]
        elif tier == "B-Tier":
            base_values = [50, 55, 50, 45, 40, 45, 50, 55, 60]
        elif tier == "C-Tier":
            base_values = [60, 50, 40, 35, 30, 25, 20, 15, 10]
        else:
            base_values = [50, 50, 50, 50, 50, 50, 50, 50, 50]
        
        # Añadir variación aleatoria
        popularity = {}
        for i, rank in enumerate(ranks):
            # Asegurar que el valor esté entre 1 y 99
            random_value = max(1, min(99, base_values[i] + random.randint(-10, 10)))
            popularity[rank] = random_value
        
        return popularity
    
    def open_official_guides(self):
        """Abrir guías oficiales en el navegador"""
        agent_lower = self.agent_name.lower().replace("/", "")
        url = f"https://playvalorant.com/es-es/agents/{agent_lower}/"
        QDesktopServices.openUrl(QUrl(url))
    
    def open_videos(self):
        """Abrir videos del agente en YouTube"""
        query = f"valorant {self.agent_name} guide"
        url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
        QDesktopServices.openUrl(QUrl(url))
    
    def open_youtube_lineups(self):
        """Abrir lineups del agente en YouTube"""
        query = f"valorant {self.agent_name} lineups"
        url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
        QDesktopServices.openUrl(QUrl(url))

class AgentBrowserDialog(QDialog):
    """Diálogo para explorar todos los agentes"""
    def __init__(self, agents_data, agent_images, parent=None):
        super().__init__(parent)
        self.agents_data = agents_data
        self.agent_images = agent_images
        self.parent_window = parent
        
        self.setWindowTitle("Explorador de Agentes")
        self.setMinimumSize(800, 600)
        self.setStyleSheet(f"""
            QDialog {{
                background-color: {VALORANT_BLUE};
            }}
            QLabel {{
                color: {VALORANT_WHITE};
            }}
            QTabWidget::pane {{
                border: 1px solid #2A3441;
                background-color: {VALORANT_LIGHT_BLUE};
                border-radius: 8px;
            }}
            QTabBar::tab {{
                background-color: {VALORANT_LIGHT_BLUE};
                color: {VALORANT_WHITE};
                border: 1px solid #2A3441;
                border-bottom: none;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                padding: 8px 12px;
                margin-right: 2px;
            }}
            QTabBar::tab:selected {{
                background-color: {VALORANT_RED};
                color: white;
            }}
            QTabBar::tab:!selected {{
                margin-top: 2px;
            }}
        """)
        
        # Layout principal
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Título
        title_label = QLabel("EXPLORADOR DE AGENTES")
        title_label.setStyleSheet(f"font-size: 24px; font-weight: bold; color: {VALORANT_RED};")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # Tabs para organizar por roles
        tab_widget = QTabWidget()
        layout.addWidget(tab_widget)
        
        # Tab para todos los agentes
        all_tab = QWidget()
        self.create_agents_grid(all_tab, None)
        tab_widget.addTab(all_tab, "Todos")
        
        # Tab para cada rol
        roles = ["Duelista", "Iniciador", "Controlador", "Centinela"]
        
        for role in roles:
            role_tab = QWidget()
            self.create_agents_grid(role_tab, role)
            tab_widget.addTab(role_tab, role)
        
        # Tab para tier list
        tier_tab = QWidget()
        self.create_tier_list_tab(tier_tab)
        tab_widget.addTab(tier_tab, "Tier List")
        
        # Botón para cerrar
        close_button = HoverButton("Cerrar")
        close_button.clicked.connect(self.accept)
        layout.addWidget(close_button)
    
    def create_agents_grid(self, tab, filter_role):
        """Crear grid de agentes filtrado por rol"""
        layout = QVBoxLayout(tab)
        
        # Scroll area para agentes
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("background-color: transparent;")
        
        # Contenedor para agentes
        container = QWidget()
        container.setStyleSheet("background-color: transparent;")
        grid = QGridLayout(container)
        grid.setContentsMargins(10, 10, 10, 10)
        grid.setSpacing(15)
        
        # Filtrar agentes por rol
        agents = []
        for agent_name, agent_data in self.agents_data.items():
            if filter_role is None or agent_data.get("role", "") == filter_role:
                agents.append((agent_name, agent_data))
        
        # Ordenar agentes por tier y luego por nombre
        tier_order = {"S-Tier": 0, "A-Tier": 1, "B-Tier": 2, "C-Tier": 3, "No clasificado": 4}
        
        def get_tier(agent_tuple):
            return tier_order.get(agent_tuple[1].get("tier", "No clasificado"), 4)
        
        agents.sort(key=lambda x: (get_tier(x), x[0]))
        
        # Añadir agentes al grid
        row, col = 0, 0
        max_cols = 4  # Número de columnas en el grid
        
        for agent_name, agent_data in agents:
            # Crear card para el agente
            agent_card = self.create_agent_card(agent_name, agent_data)
            
            grid.addWidget(agent_card, row, col)
            
            # Actualizar fila y columna
            col += 1
            if col >= max_cols:
                col = 0
                row += 1
        
        scroll.setWidget(container)
        layout.addWidget(scroll)
    
    def create_agent_card(self, agent_name, agent_data):
        """Crear tarjeta para un agente"""
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {VALORANT_LIGHT_BLUE};
                border-radius: 8px;
                padding: 10px;
            }}
            QFrame:hover {{
                background-color: #2A3441;
                border: 1px solid {VALORANT_RED};
            }}
        """)
        card.setCursor(QCursor(Qt.PointingHandCursor))
        
        # Layout
        layout = QVBoxLayout(card)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(5)
        
        # Imagen del agente
        image_label = QLabel()
        image_label.setAlignment(Qt.AlignCenter)
        
        if agent_name in self.agent_images and self.agent_images[agent_name]:
            pixmap = QPixmap.fromImage(self.agent_images[agent_name])
            pixmap = pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            image_label.setPixmap(pixmap)
        else:
            # Crear imagen de placeholder
            self.create_placeholder_image(image_label, agent_name, agent_data)
        
        layout.addWidget(image_label)
        
        # Nombre del agente
        name_label = QLabel(agent_name)
        name_label.setStyleSheet("font-size: 14px; font-weight: bold; color: white;")
        name_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(name_label)
        
        # Rol del agente
        role = agent_data.get("role", "Desconocido")
        role_color = ROLE_COLORS.get(role, VALORANT_WHITE)
        
        role_label = QLabel(role)
        role_label.setStyleSheet(f"font-size: 12px; color: {role_color};")
        role_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(role_label)
        
        # Tier del agente
        tier = agent_data.get("tier", "No clasificado")
        tier_color = TIER_COLORS.get(tier, VALORANT_WHITE)
        
        tier_label = QLabel(tier)
        tier_label.setStyleSheet(f"font-size: 12px; color: {tier_color};")
        tier_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(tier_label)
        
        # Botón de ver detalles
        details_button = HoverButton("Ver Detalles", color="#1F2731")
        details_button.clicked.connect(lambda: self.show_agent_details(agent_name))
        layout.addWidget(details_button)
        
        return card
    
    def create_placeholder_image(self, label, agent_name, agent_data):
        """Crear imagen de placeholder para el agente"""
        role = agent_data.get("role", "Desconocido")
        color = ROLE_COLORS.get(role, VALORANT_WHITE)
        
        # Crear imagen
        image = QImage(100, 100, QImage.Format_ARGB32)
        image.fill(QColor(VALORANT_BLUE))
        
        painter = QPainter(image)
        painter.setPen(QColor(color))
        painter.setBrush(QColor(color).darker(150))
        painter.drawRoundedRect(5, 5, 90, 90, 10, 10)
        
        # Añadir texto
        painter.setPen(QColor(VALORANT_WHITE))
        font = QFont("Arial", 14, QFont.Bold)
        painter.setFont(font)
        painter.drawText(QRect(5, 5, 90, 90), Qt.AlignCenter, agent_name)
        painter.end()
        
        # Establecer la imagen
        label.setPixmap(QPixmap.fromImage(image))
    
    def create_tier_list_tab(self, tab):
        """Crear tab de tier list"""
        layout = QVBoxLayout(tab)
        
        # Scroll area para tier list
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("background-color: transparent;")
        
        # Contenedor para tier list
        container = QWidget()
        container.setStyleSheet("background-color: transparent;")
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(10, 10, 10, 10)
        container_layout.setSpacing(20)
        
        # Título
        title_label = QLabel("TIER LIST DE AGENTES")
        title_label.setStyleSheet(f"font-size: 18px; font-weight: bold; color: {VALORANT_RED};")
        title_label.setAlignment(Qt.AlignCenter)
        container_layout.addWidget(title_label)
        
        # Descripción
        desc_label = QLabel("Esta tier list está basada en la meta actual y puede cambiar con actualizaciones del juego.")
        desc_label.setStyleSheet("font-size: 12px; font-style: italic;")
        desc_label.setAlignment(Qt.AlignCenter)
        desc_label.setWordWrap(True)
        container_layout.addWidget(desc_label)
        
        # Crear secciones para cada tier
        tiers = ["S-Tier", "A-Tier", "B-Tier", "C-Tier"]
        
        for tier in tiers:
            # Frame para el tier
            tier_frame = QFrame()
            tier_frame.setStyleSheet(f"""
                background-color: {VALORANT_LIGHT_BLUE};
                border-radius: 8px;
                padding: 10px;
            """)
            tier_layout = QVBoxLayout(tier_frame)
            
            # Título del tier
            tier_color = TIER_COLORS.get(tier, VALORANT_WHITE)
            tier_title = QLabel(tier)
            tier_title.setStyleSheet(f"font-size: 16px; font-weight: bold; color: {tier_color};")
            tier_layout.addWidget(tier_title)
            
            # Descripción del tier
            tier_desc = self.get_tier_description(tier)
            desc_label = QLabel(tier_desc)
            desc_label.setStyleSheet("font-size: 12px;")
            desc_label.setWordWrap(True)
            tier_layout.addWidget(desc_label)
            
            # Grid para agentes de este tier
            agents_frame = QFrame()
            agents_layout = QGridLayout(agents_frame)
            agents_layout.setContentsMargins(0, 10, 0, 0)
            agents_layout.setSpacing(10)
            
            # Filtrar agentes por tier
            tier_agents = []
            for agent_name, agent_data in self.agents_data.items():
                if agent_data.get("tier", "") == tier:
                    tier_agents.append((agent_name, agent_data))
            
            # Ordenar agentes por nombre
            tier_agents.sort(key=lambda x: x[0])
            
            # Añadir agentes al grid
            row, col = 0, 0
            max_cols = 5  # Número de columnas en el grid
            
            for agent_name, agent_data in tier_agents:
                # Crear mini card para el agente
                agent_card = self.create_mini_agent_card(agent_name, agent_data)
                
                agents_layout.addWidget(agent_card, row, col)
                
                # Actualizar fila y columna
                col += 1
                if col >= max_cols:
                    col = 0
                    row += 1
            
            tier_layout.addWidget(agents_frame)
            container_layout.addWidget(tier_frame)
        
        scroll.setWidget(container)
        layout.addWidget(scroll)
    
    def create_mini_agent_card(self, agent_name, agent_data):
        """Crear mini tarjeta para un agente en la tier list"""
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: #2A3441;
                border-radius: 4px;
                padding: 5px;
            }}
            QFrame:hover {{
                background-color: #3A4451;
                border: 1px solid {VALORANT_RED};
            }}
        """)
        card.setCursor(QCursor(Qt.PointingHandCursor))
        
        # Layout
        layout = QHBoxLayout(card)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)
        
        # Imagen del agente (pequeña)
        image_label = QLabel()
        image_label.setFixedSize(30, 30)
        
        if agent_name in self.agent_images and self.agent_images[agent_name]:
            pixmap = QPixmap.fromImage(self.agent_images[agent_name])
            pixmap = pixmap.scaled(30, 30, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            image_label.setPixmap(pixmap)
        else:
            # Usar solo el texto para mini cards
            image_label.setText(agent_name[0])
            image_label.setStyleSheet(f"font-size: 14px; font-weight: bold; color: {VALORANT_WHITE}; background-color: {VALORANT_BLUE}; border-radius: 15px;")
            image_label.setAlignment(Qt.AlignCenter)
        
        layout.addWidget(image_label)
        
        # Nombre del agente
        name_label = QLabel(agent_name)
        name_label.setStyleSheet("font-size: 12px; color: white;")
        layout.addWidget(name_label)
        
        # Conectar clic para mostrar detalles
        card.mousePressEvent = lambda event: self.show_agent_details(agent_name)
        
        return card
    
    def get_tier_description(self, tier):
        """Obtener descripción para cada tier"""
        descriptions = {
            "S-Tier": "Agentes meta dominantes, extremadamente efectivos en el parche actual. Son considerados imprescindibles en la mayoría de composiciones.",
            "A-Tier": "Agentes muy fuertes y versátiles en la mayoría de mapas y composiciones. Excelentes opciones para cualquier equipo.",
            "B-Tier": "Agentes sólidos pero situacionales o que requieren mayor coordinación. Pueden brillar en mapas o composiciones específicas.",
            "C-Tier": "Agentes que actualmente están en desventaja en la meta o requieren buffs. Pueden ser efectivos en manos expertas pero generalmente hay mejores alternativas."
        }
        
        return descriptions.get(tier, "")
    
    def show_agent_details(self, agent_name):
        """Mostrar detalles del agente"""
        agent_data = self.agents_data.get(agent_name, {})
        agent_image = self.agent_images.get(agent_name)
        
        dialog = AgentInfoDialog(agent_name, agent_data, agent_image, self)
        dialog.exec_()

class ValorantTeamCompAdvisor(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Configuración de la ventana principal
        self.setWindowTitle("Valorant Team Comp Advisor Premium")
        self.setMinimumSize(1200, 800)
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {VALORANT_BLUE};
            }}
            QLabel {{
                color: {VALORANT_WHITE};
            }}
            QScrollArea {{
                border: none;
                background-color: transparent;
            }}
            QGroupBox {{
                border: 1px solid #2A3441;
                border-radius: 8px;
                margin-top: 1ex;
                font-weight: bold;
                color: {VALORANT_WHITE};
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 5px;
            }}
            QComboBox {{
                background-color: {VALORANT_LIGHT_BLUE};
                color: {VALORANT_WHITE};
                border: 1px solid #2A3441;
                border-radius: 4px;
                padding: 5px;
            }}
            QComboBox::drop-down {{
                border: none;
            }}
            QComboBox QAbstractItemView {{
                background-color: {VALORANT_LIGHT_BLUE};
                color: {VALORANT_WHITE};
                selection-background-color: #2A3441;
            }}
            QToolBar {{
                background-color: {VALORANT_LIGHT_BLUE};
                border: none;
            }}
            QToolButton {{
                background-color: transparent;
                border: none;
                color: {VALORANT_WHITE};
            }}
            QToolButton:hover {{
                background-color: #2A3441;
            }}
            QMenu {{
                background-color: {VALORANT_LIGHT_BLUE};
                color: {VALORANT_WHITE};
                border: 1px solid #2A3441;
            }}
            QMenu::item {{
                padding: 5px 20px 5px 20px;
            }}
            QMenu::item:selected {{
                background-color: #2A3441;
            }}
            QStatusBar {{
                background-color: {VALORANT_LIGHT_BLUE};
                color: {VALORANT_WHITE};
            }}
        """)
        
        # Variables de estado
        self.selected_map = None
        self.selected_agent = None
        self.comp_style = "Balanceada"
        self.agent_cards = {}
        self.map_cards = {}
        self.composition_history = []
        self.size_factor = 1.0  # Factor de escala para elementos responsivos
        
        # Cargar datos
        self.load_data()
        
        # Crear la interfaz
        self.create_ui()
        
        # Mostrar mensaje de bienvenida
        self.show_welcome_message()
        
        # Configurar eventos de redimensionamiento
        self.resizeEvent = self.on_resize
    
    def load_data(self):
        """Cargar datos de agentes, mapas y composiciones"""
        # Agents by role data
        self.agents_by_role = {
            "Duelista": ["Jett", "Raze", "Phoenix", "Reyna", "Neon", "Yoru", "Iso"],
            "Iniciador": ["Sova", "Breach", "Skye", "KAY/O", "Fade", "Gekko", "Tejo", "Waylay"],
            "Controlador": ["Brimstone", "Viper", "Omen", "Astra", "Harbor", "Clove"],
            "Centinela": ["Killjoy", "Cypher", "Sage", "Chamber", "Deadlock", "Vyse"]
        }
        
        # Maps data
        self.maps = [
            "Ascent", "Bind", "Breeze", "Fracture", "Haven", 
            "Icebox", "Lotus", "Pearl", "Split", "Sunset"
        ]
        
        # Map-specific optimal comps
        self.map_comps = {
            "Ascent": {
                "pro": ["Jett", "Omen", "Sova", "KAY/O", "Killjoy"],
                "ranked": ["Jett", "Omen", "Sova", "KAY/O", "Killjoy"],
                "alt": ["Jett", "Omen", "Skye", "Reyna", "Killjoy"],
                "aggressive": ["Jett", "Reyna", "Raze", "Skye", "Omen"],
                "defensive": ["Cypher", "Killjoy", "Sage", "Sova", "Omen"],
                "description": "Equilibra poder de entrada, control de mapa e información. Jett aporta entrada rápida y uso del Operator, Omen controla ángulos con sus humos, los iniciadores brindan reconocimiento, y Killjoy asegura la defensa de sitios."
            },
            "Bind": {
                "pro": ["Raze", "Skye", "Brimstone", "Viper", "Cypher"],
                "ranked": ["Raze", "Skye", "Brimstone", "Viper", "Killjoy"],
                "alt": ["Phoenix", "Fade", "Brimstone", "Viper", "Cypher"],
                "aggressive": ["Raze", "Phoenix", "Skye", "Breach", "Brimstone"],
                "defensive": ["Cypher", "Killjoy", "Viper", "Brimstone", "Sova"],
                "description": "Mapa con teletransportadores que requiere control de flancos. Raze es excelente para limpiar espacios cerrados, Brimstone y Viper controlan sitios con humos, mientras Cypher vigila los flancos y teletransportadores."
            },
            "Breeze": {
                "pro": ["Jett", "Sova", "Viper", "Chamber", "Skye"],
                "ranked": ["Jett", "Sova", "Viper", "Killjoy", "Skye"],
                "alt": ["Jett", "Sova", "Viper", "Cypher", "KAY/O"],
                "aggressive": ["Jett", "Reyna", "Skye", "Sova", "Viper"],
                "defensive": ["Chamber", "Viper", "Cypher", "Sova", "Omen"],
                "description": "Mapa amplio con largas líneas de visión. Viper es esencial para dividir espacios abiertos, Jett y Chamber aprovechan las líneas largas con Operator, mientras Sova y Skye proporcionan información crucial."
            },
            "Fracture": {
                "pro": ["Raze", "Breach", "Brimstone", "Fade", "Chamber"],
                "ranked": ["Raze", "Breach", "Brimstone", "Fade", "Killjoy"],
                "alt": ["Neon", "Breach", "Brimstone", "Fade", "Cypher"],
                "aggressive": ["Raze", "Neon", "Breach", "Fade", "Brimstone"],
                "defensive": ["Chamber", "Cypher", "Breach", "Fade", "Brimstone"],
                "description": "Composición con alto poder de iniciadores y utilidades de control. Raze aprovecha los ángulos cerrados, Breach y Fade proporcionan un combo de aturdimiento y revelado, Brimstone coloca humos rápidos, mientras el centinela controla flancos."
            },
            "Haven": {
                "pro": ["Jett", "Sova", "Omen", "Cypher", "Breach"],
                "ranked": ["Jett", "Sova", "Omen", "Killjoy", "Breach"],
                "alt": ["Jett", "Sova", "Omen", "Killjoy", "KAY/O"],
                "aggressive": ["Jett", "Reyna", "Breach", "Skye", "Omen"],
                "defensive": ["Cypher", "Killjoy", "Sova", "Sage", "Omen"],
                "description": "Al tener tres sitios, exige una composición versátil. Jett es imprescindible para aprovechar las largas líneas de visión, Omen cubre múltiples ángulos, la combinación de Sova y Breach provee información constante, mientras el centinela ofrece control de flancos."
            },
            "Icebox": {
                "pro": ["Jett", "Sova", "Viper", "Sage", "Killjoy"],
                "ranked": ["Jett", "Sova", "Viper", "Sage", "Killjoy"],
                "alt": ["Reyna", "Sova", "Viper", "Sage", "Chamber"],
                "aggressive": ["Jett", "Reyna", "Sova", "Viper", "Sage"],
                "defensive": ["Killjoy", "Sage", "Viper", "Sova", "Chamber"],
                "description": "Viper es imprescindible, dividiendo sitios con su Pantalla Tóxica. Sage proporciona muro para plantar (especialmente en B) y orbes lentos. Sova despejar espacios largos. Jett puede tomar ángulos elevados. Killjoy vigila flancos en este mapa de amplias rotaciones."
            },
            "Lotus": {
                "pro": ["Raze", "Fade", "Omen", "Viper", "Killjoy"],
                "ranked": ["Raze", "Fade", "Omen", "Viper", "Killjoy"],
                "alt": ["Jett", "Skye", "Omen", "Viper", "Killjoy"],
                "aggressive": ["Raze", "Jett", "Fade", "Skye", "Omen"],
                "defensive": ["Killjoy", "Cypher", "Viper", "Omen", "Fade"],
                "description": "La dupla de controladores Omen + Viper es clave. Raze limpia esquinas estrechas y zonas de las puertas. Fade explora los amplios espacios y conectores del mapa. Killjoy vigila rotaciones a través de las puertas y su definitiva cubre áreas extensas."
            },
            "Pearl": {
                "pro": ["Jett", "Fade", "Astra", "Chamber", "Sage"],
                "ranked": ["Jett", "Fade", "Astra", "Killjoy", "Sage"],
                "alt": ["Neon", "KAY/O", "Astra", "Killjoy", "Sage"],
                "aggressive": ["Jett", "Neon", "Fade", "Skye", "Astra"],
                "defensive": ["Chamber", "Killjoy", "Sage", "Astra", "Fade"],
                "description": "Astra con sus humos globales puede tapar ángulos largos. Fade revela enemigos en rincones. Chamber vigila flancos y su definitiva es letal en largas distancias. Jett infiltra y toma duelos de larga distancia. Sage controla Mid Connector o bloquea A Main."
            },
            "Split": {
                "pro": ["Raze", "Skye", "Omen", "Cypher", "Sage"],
                "ranked": ["Raze", "Skye", "Omen", "Killjoy", "Sage"],
                "alt": ["Jett", "Raze", "Omen", "Skye", "Sage"],
                "aggressive": ["Raze", "Jett", "Breach", "Skye", "Omen"],
                "defensive": ["Cypher", "Killjoy", "Sage", "Omen", "Skye"],
                "description": "Raze aprovecha sus Blast Packs y granadas en entradas cortas. Skye usa destellos y trailblazer para limpiar esquinas. Omen bloquea visibilidad en puntos clave. Cypher coloca trampas en flancos. Sage levanta muros que bloquean rutas cruciales y ralentiza pushes."
            },
            "Sunset": {
                "pro": ["Raze", "Skye", "Omen", "Deadlock", "Killjoy"],
                "ranked": ["Raze", "Skye", "Omen", "Deadlock", "Killjoy"],
                "alt": ["Phoenix", "Fade", "Brimstone", "Deadlock", "Killjoy"],
                "aggressive": ["Raze", "Phoenix", "Skye", "Omen", "Deadlock"],
                "defensive": ["Deadlock", "Killjoy", "Cypher", "Omen", "Skye"],
                "description": "Mapa con múltiples niveles y ángulos verticales. Raze y Phoenix son excelentes para limpiar espacios cerrados, Deadlock controla áreas clave, mientras Killjoy asegura el control de sitios con su utilidad."
            }
        }
        
        # Tier list data
        self.tier_list = {
            "S-Tier": ["Tejo", "Clove", "Raze", "Vyse"],
            "A-Tier": ["Yoru", "Deadlock", "Cypher", "Jett", "Iso", "Neon", "Sova", "Gekko", 
                      "Killjoy", "Omen", "Brimstone", "Phoenix", "Sage"],
            "B-Tier": ["Chamber", "Viper", "Breach", "Skye", "Fade", "Astra", "Reyna"],
            "C-Tier": ["Waylay", "KAY/O", "Harbor"]
        }
        
        # Agent roles mapping
        self.agent_roles = {}
        for role, agents in self.agents_by_role.items():
            for agent in agents:
                self.agent_roles[agent] = role
        
        # Get all agents for selection
        self.all_agents = []
        for role_agents in self.agents_by_role.values():
            self.all_agents.extend(role_agents)
        self.all_agents.sort()
        
        # Agent abilities and descriptions
        self.agent_details = {}
        
        # Crear datos detallados para cada agente
        for agent in self.all_agents:
            # Obtener rol
            role = self.agent_roles.get(agent, "Desconocido")
            
            # Obtener tier
            tier = "No clasificado"
            for t, agents in self.tier_list.items():
                if agent in agents:
                    tier = t
            
            # Crear datos básicos
            self.agent_details[agent] = {
                "role": role,
                "tier": tier,
                "abilities": self.generate_abilities(agent, role),
                "description": self.generate_description(agent, role)
            }
        
        # Añadir datos específicos para algunos agentes
        if "Jett" in self.agent_details:
            self.agent_details["Jett"].update({
                "real_name": "Sunwoo Han",
                "origin": "Corea del Sur",
                "playstyle": "Agresivo, entrada rápida, operador",
                "description": "Agente ágil con gran movilidad, perfecta para entradas rápidas y uso del Operator."
            })
        
        if "Raze" in self.agent_details:
            self.agent_details["Raze"].update({
                "real_name": "Tayane Alves",
                "origin": "Brasil",
                "playstyle": "Agresivo, daño por área, vertical",
                "description": "Especialista en daño explosivo, excelente para limpiar espacios cerrados y movimiento vertical."
            })
        
        if "Sova" in self.agent_details:
            self.agent_details["Sova"].update({
                "real_name": "Sasha Novikov",
                "origin": "Rusia",
                "playstyle": "Reconocimiento, información, apoyo",
                "description": "Maestro del reconocimiento, proporciona información crucial para el equipo con sus flechas y drone."
            })
        
        # Map callouts and strategies
        self.map_details = {
            "Ascent": {
                "location": "Italia",
                "callouts": ["A Main", "A Lobby", "Catwalk", "Heaven", "Hell", "Mid", "Market", "B Main"],
                "attack_strategies": [
                    "Tomar control de Mid para dividir defensas",
                    "Ejecutar rápido en A con humos en Heaven y Hell",
                    "Fake A, rotación a B a través de Market"
                ],
                "defense_strategies": [
                    "Mantener control de Mid con operador",
                    "Utilidad de Killjoy en B para retrasar pushes",
                    "Jugar retake en A con utilidad guardada"
                ]
            },
            # Añadir más mapas según sea necesario
        }
        
        # Cargar imágenes
        self.load_images()
    
    def generate_abilities(self, agent, role):
        """Generar habilidades simuladas para un agente"""
        # Habilidades conocidas para algunos agentes
        known_abilities = {
            "Jett": ["Tailwind", "Cloudburst", "Updraft", "Blade Storm"],
            "Raze": ["Blast Pack", "Paint Shells", "Boom Bot", "Showstopper"],
            "Sova": ["Shock Bolt", "Recon Bolt", "Owl Drone", "Hunter's Fury"],
            "Omen": ["Paranoia", "Dark Cover", "Shrouded Step", "From the Shadows"],
            "Killjoy": ["Alarmbot", "Turret", "Nanoswarm", "Lockdown"],
            "Viper": ["Poison Cloud", "Toxic Screen", "Snake Bite", "Viper's Pit"],
            "Cypher": ["Cyber Cage", "Spycam", "Trapwire", "Neural Theft"],
            "Sage": ["Slow Orb", "Healing Orb", "Barrier Orb", "Resurrection"],
            "Phoenix": ["Curveball", "Hot Hands", "Blaze", "Run it Back"],
            "Breach": ["Flashpoint", "Fault Line", "Aftershock", "Rolling Thunder"]
        }
        
        if agent in known_abilities:
            return known_abilities[agent]
        
        # Generar habilidades genéricas basadas en el rol
        if role == "Duelista":
            return ["Flash", "Movilidad", "Daño", "Ultimate (Daño/Movilidad)"]
        elif role == "Iniciador":
            return ["Reconocimiento", "Flash/Cegadora", "Daño/Debilitación", "Ultimate (Información/Daño)"]
        elif role == "Controlador":
            return ["Humo 1", "Humo 2", "Utilidad de Control", "Ultimate (Control de Área)"]
        elif role == "Centinela":
            return ["Trampa 1", "Trampa 2", "Utilidad Defensiva", "Ultimate (Información/Defensa)"]
        else:
            return ["Habilidad 1", "Habilidad 2", "Habilidad 3", "Ultimate"]
    
    def generate_description(self, agent, role):
        """Generar descripción simulada para un agente"""
        if role == "Duelista":
            return f"{agent} es un duelista diseñado para crear espacio y tomar duelos agresivos. Sus habilidades le permiten entrar rápidamente a los sitios y crear ventajas para su equipo."
        elif role == "Iniciador":
            return f"{agent} es un iniciador especializado en recopilar información y preparar entradas. Sus habilidades revelan posiciones enemigas y facilitan el trabajo de los duelistas."
        elif role == "Controlador":
            return f"{agent} es un controlador que domina el campo de batalla con humos y habilidades de control de área. Puede bloquear líneas de visión y dividir sitios estratégicamente."
        elif role == "Centinela":
            return f"{agent} es un centinela enfocado en defender sitios y vigilar flancos. Sus trampas y utilidad defensiva son cruciales para mantener el control del mapa."
        else:
            return f"Información no disponible para {agent}."
    
    def load_images(self):
        """Cargar imágenes de agentes y mapas"""
        self.agent_images = {}
        self.map_images = {}
        
        try:
            images_dir = "imagenes"
            
            # Verificar si existe el directorio de imágenes
            if not os.path.exists(images_dir):
                os.makedirs(images_dir)
                print(f"Directorio de imágenes creado: {images_dir}")
            
            # Cargar imágenes de agentes
            for agent in self.all_agents:
                agent_lower = agent.lower().replace("/", "")  # Manejar KAY/O
                
                try:
                    img_path = os.path.join(images_dir, f"{agent_lower}.png")
                    if os.path.exists(img_path):
                        image = QImage(img_path)
                        self.agent_images[agent] = image
                    else:
                        # Crear imagen de placeholder
                        self.agent_images[agent] = None
                except Exception as e:
                    print(f"Error cargando imagen para {agent}: {e}")
                    self.agent_images[agent] = None
            
            # Cargar imágenes de mapas
            for map_name in self.maps:
                map_lower = map_name.lower()
                
                try:
                    img_path = os.path.join(images_dir, f"{map_lower}.png")
                    if os.path.exists(img_path):
                        image = QImage(img_path)
                        self.map_images[map_name] = image
                    else:
                        # Crear imagen de placeholder
                        self.map_images[map_name] = None
                except Exception as e:
                    print(f"Error cargando imagen para el mapa {map_name}: {e}")
                    self.map_images[map_name] = None
                    
        except Exception as e:
            print(f"Error cargando imágenes: {e}")
            QMessageBox.warning(self, "Error de Imágenes", 
                              "No se pudieron cargar algunas imágenes. " +
                              "Asegúrate de tener la carpeta 'imagenes' en el mismo directorio que el programa.")
    
    def create_ui(self):
        """Crear la interfaz de usuario"""
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # Crear barra de herramientas
        self.create_toolbar()
        
        # Crear cabecera
        self.create_header(main_layout)
        
        # Crear contenido principal (splitter para panel de selección y resultados)
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter, 1)  # 1 = stretch factor
        
        # Panel de selección (izquierda)
        selection_panel = QWidget()
        selection_layout = QVBoxLayout(selection_panel)
        selection_layout.setContentsMargins(0, 0, 0, 0)
        selection_layout.setSpacing(10)
        
        # Crear secciones del panel de selección
        self.create_map_selection(selection_layout)
        self.create_agent_selection(selection_layout)
        self.create_comp_preferences(selection_layout)
        
        # Botones de acción
        buttons_frame = QFrame()
        buttons_layout = QVBoxLayout(buttons_frame)
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        buttons_layout.setSpacing(10)
        
        # Botón de generar
        generate_button = HoverButton("OBTENER COMPOSICIÓN")
        generate_button.setMinimumHeight(50)
        generate_button.setStyleSheet(f"""
            font-size: 14px;
            font-weight: bold;
        """)
        generate_button.clicked.connect(self.generate_composition)
        buttons_layout.addWidget(generate_button)
        
        # Botón de guardar composición
        save_button = HoverButton("GUARDAR COMPOSICIÓN", color=VALORANT_LIGHT_BLUE)
        save_button.clicked.connect(self.save_composition)
        buttons_layout.addWidget(save_button)
        
        # Botón de explorar agentes
        explore_button = HoverButton("EXPLORAR AGENTES", color=VALORANT_LIGHT_BLUE)
        explore_button.clicked.connect(self.show_agent_browser)
        buttons_layout.addWidget(explore_button)
        
        selection_layout.addWidget(buttons_frame)
        
        # Añadir panel de selección al splitter
        splitter.addWidget(selection_panel)
        
        # Panel de resultados (derecha)
        self.results_panel = QWidget()
        results_layout = QVBoxLayout(self.results_panel)
        results_layout.setContentsMargins(0, 0, 0, 0)
        results_layout.setSpacing(10)
        
        # Cabecera de resultados
        results_header = QLabel("COMPOSICIÓN RECOMENDADA")
        results_header.setStyleSheet(f"font-size: 18px; font-weight: bold; color: {VALORANT_RED};")
        results_header.setAlignment(Qt.AlignCenter)
        results_layout.addWidget(results_header)
        
        # Área de resultados con scroll
        self.results_scroll = QScrollArea()
        self.results_scroll.setWidgetResizable(True)
        self.results_scroll.setFrameShape(QFrame.NoFrame)
        
        # Contenido de resultados
        self.results_content = QWidget()
        self.results_content_layout = QVBoxLayout(self.results_content)
        self.results_content_layout.setAlignment(Qt.AlignTop)
        self.results_content_layout.setContentsMargins(10, 10, 10, 10)
        self.results_content_layout.setSpacing(15)
        
        self.results_scroll.setWidget(self.results_content)
        results_layout.addWidget(self.results_scroll)
        
        # Añadir panel de resultados al splitter
        splitter.addWidget(self.results_panel)
        
        # Establecer proporciones del splitter (40% izquierda, 60% derecha)
        splitter.setSizes([400, 600])
        
        # Crear pie de página
        self.create_footer(main_layout)
        
        # Crear barra de estado
        self.statusBar().showMessage("Listo para generar composiciones")
    
    def create_toolbar(self):
        """Crear barra de herramientas"""
        toolbar = QToolBar("Barra de herramientas")
        toolbar.setMovable(False)
        toolbar.setIconSize(QSize(16, 16))
        self.addToolBar(toolbar)
        
        # Acción de ayuda
        help_action = QAction("Ayuda", self)
        help_action.triggered.connect(self.show_help)
        toolbar.addAction(help_action)
        
        # Acción de acerca de
        about_action = QAction("Acerca de", self)
        about_action.triggered.connect(self.show_about)
        toolbar.addAction(about_action)
        
        # Separador
        toolbar.addSeparator()
        
        # Acción de historial
        history_action = QAction("Historial", self)
        history_action.triggered.connect(self.show_history)
        toolbar.addAction(history_action)
        
        # Acción de exportar
        export_action = QAction("Exportar", self)
        export_action.triggered.connect(self.export_composition)
        toolbar.addAction(export_action)
        
        # Acción de explorar agentes
        explore_action = QAction("Explorar Agentes", self)
        explore_action.triggered.connect(self.show_agent_browser)
        toolbar.addAction(explore_action)
        
        # Añadir espaciador para alinear a la derecha
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        toolbar.addWidget(spacer)
        
        # Acción de salir
        exit_action = QAction("Salir", self)
        exit_action.triggered.connect(self.close)
        toolbar.addAction(exit_action)
    
    def create_header(self, layout):
        """Crear cabecera de la aplicación"""
        header_frame = QFrame()
        header_frame.setStyleSheet(f"background-color: {VALORANT_BLUE};")
        header_layout = QHBoxLayout(header_frame)
        
        # Logo y título
        title_label = QLabel("VALORANT TEAM COMP ADVISOR PREMIUM")
        title_label.setStyleSheet(f"font-size: 24px; font-weight: bold; color: {VALORANT_RED};")
        header_layout.addWidget(title_label)
        
        # Versión
        version_label = QLabel("v3.0")
        version_label.setStyleSheet(f"font-size: 12px; color: {VALORANT_ACCENT};")
        version_label.setAlignment(Qt.AlignBottom)
        header_layout.addWidget(version_label)
        
        # Añadir espaciador para alinear a la derecha
        header_layout.addStretch()
        
        # Añadir cabecera al layout principal
        layout.addWidget(header_frame)
    
    def create_map_selection(self, layout):
        """Crear sección de selección de mapa"""
        map_group = QGroupBox("SELECCIÓN DE MAPA")
        map_group.setStyleSheet(f"""
            QGroupBox {{
                background-color: {VALORANT_LIGHT_BLUE};
                padding: 15px;
            }}
        """)
        map_layout = QVBoxLayout(map_group)
        
        # Scroll area para mapas
        map_scroll = QScrollArea()
        map_scroll.setWidgetResizable(True)
        map_scroll.setFrameShape(QFrame.NoFrame)
        map_scroll.setStyleSheet("background-color: transparent;")
        
        # Contenedor de mapas
        map_container = QWidget()
        map_container.setStyleSheet("background-color: transparent;")
        map_grid = QGridLayout(map_container)
        map_grid.setContentsMargins(5, 5, 5, 5)
        map_grid.setSpacing(10)
        
        # Añadir mapas al grid
        row, col = 0, 0
        for map_name in self.maps:
            map_card = MapCard(map_name, self.map_images.get(map_name), size_factor=self.size_factor)
            map_card.clicked.connect(self.on_map_selected)
            self.map_cards[map_name] = map_card
            
            map_grid.addWidget(map_card, row, col)
            
            # Actualizar fila y columna
            col += 1
            if col > 1:  # 2 columnas
                col = 0
                row += 1
        
        map_scroll.setWidget(map_container)
        map_layout.addWidget(map_scroll)
        
        # Etiqueta de mapa seleccionado
        self.selected_map_label = QLabel("Mapa seleccionado: Ninguno")
        self.selected_map_label.setStyleSheet("font-weight: bold; padding: 5px;")
        self.selected_map_label.setAlignment(Qt.AlignCenter)
        map_layout.addWidget(self.selected_map_label)
        
        # Añadir grupo de mapas al layout principal
        layout.addWidget(map_group)
    
    def create_agent_selection(self, layout):
        """Crear sección de selección de agente"""
        agent_group = QGroupBox("SELECCIÓN DE AGENTE")
        agent_group.setStyleSheet(f"""
            QGroupBox {{
                background-color: {VALORANT_LIGHT_BLUE};
                padding: 15px;
            }}
        """)
        agent_layout = QVBoxLayout(agent_group)
        
        # Filtros de rol
        role_frame = QFrame()
        role_frame.setStyleSheet("background-color: transparent;")
        role_layout = QHBoxLayout(role_frame)
        role_layout.setContentsMargins(0, 0, 0, 10)
        
        # Botones de filtro por rol
        self.role_buttons = {}
        
        for role in ["Todos"] + list(self.agents_by_role.keys()):
            btn = RoleButton(role)
            btn.clicked.connect(lambda checked, r=role: self.filter_agents_by_role(r))
            role_layout.addWidget(btn)
            self.role_buttons[role] = btn
        
        agent_layout.addWidget(role_frame)
        
        # Scroll area para agentes
        agent_scroll = QScrollArea()
        agent_scroll.setWidgetResizable(True)
        agent_scroll.setFrameShape(QFrame.NoFrame)
        agent_scroll.setStyleSheet("background-color: transparent;")
        
        # Contenedor de agentes
        self.agent_container = QWidget()
        self.agent_container.setStyleSheet("background-color: transparent;")
        self.agent_grid = QGridLayout(self.agent_container)
        self.agent_grid.setContentsMargins(5, 5, 5, 5)
        self.agent_grid.setSpacing(10)
        
        # Poblar agentes
        self.populate_agents()
        
        agent_scroll.setWidget(self.agent_container)
        agent_layout.addWidget(agent_scroll)
        
        # Etiqueta de agente seleccionado
        self.selected_agent_label = QLabel("Agente seleccionado: Ninguno")
        self.selected_agent_label.setStyleSheet("font-weight: bold; padding: 5px;")
        self.selected_agent_label.setAlignment(Qt.AlignCenter)
        agent_layout.addWidget(self.selected_agent_label)
        
        # Añadir grupo de agentes al layout principal
        layout.addWidget(agent_group)
    
    def create_comp_preferences(self, layout):
        """Crear sección de preferencias de composición"""
        pref_group = QGroupBox("PREFERENCIAS")
        pref_group.setStyleSheet(f"""
            QGroupBox {{
                background-color: {VALORANT_LIGHT_BLUE};
                padding: 15px;
            }}
        """)
        pref_layout = QVBoxLayout(pref_group)
        
        # Estilo de juego
        style_frame = QFrame()
        style_frame.setStyleSheet("background-color: transparent;")
        style_layout = QHBoxLayout(style_frame)
        style_layout.setContentsMargins(0, 0, 0, 0)
        
        style_label = QLabel("Estilo de juego:")
        style_label.setStyleSheet("font-weight: bold;")
        style_layout.addWidget(style_label)
        
        # Grupo de botones de radio
        self.style_group = QButtonGroup(self)
        
        for style in ["Balanceada", "Agresiva", "Defensiva"]:
            radio = StyleRadioButton(style)
            if style == "Balanceada":
                radio.setChecked(True)
            radio.toggled.connect(lambda checked, s=style: self.on_style_changed(s) if checked else None)
            style_layout.addWidget(radio)
            self.style_group.addButton(radio)
        
        pref_layout.addWidget(style_frame)
        
        # Añadir grupo de preferencias al layout principal
        layout.addWidget(pref_group)
    
    def create_footer(self, layout):
        """Crear pie de página"""
        footer_frame = QFrame()
        footer_frame.setStyleSheet(f"background-color: {VALORANT_BLUE};")
        footer_layout = QHBoxLayout(footer_frame)
        
        # Texto de actualización
        update_label = QLabel("Desarrollado con datos de meta actualizados a mayo 2025")
        update_label.setStyleSheet(f"font-size: 10px; color: {VALORANT_ACCENT};")
        footer_layout.addWidget(update_label)
        
        # Añadir espaciador para alinear a la derecha
        footer_layout.addStretch()
        
        # Enlace a la web oficial
        web_link = QLabel("valorant.com")
        web_link.setStyleSheet(f"font-size: 10px; color: {VALORANT_RED}; text-decoration: underline;")
        web_link.setCursor(QCursor(Qt.PointingHandCursor))
        web_link.mousePressEvent = lambda e: QDesktopServices.openUrl(QUrl("https://playvalorant.com/"))
        footer_layout.addWidget(web_link)
        
        # Añadir pie de página al layout principal
        layout.addWidget(footer_frame)
    
    def populate_agents(self, filter_role="Todos"):
        """Poblar la cuadrícula de agentes según el filtro de rol"""
        # Limpiar grid
        for i in reversed(range(self.agent_grid.count())):
            self.agent_grid.itemAt(i).widget().setParent(None)
        
        # Filtrar agentes por rol
        if filter_role == "Todos":
            agents_to_show = self.all_agents
        else:
            agents_to_show = self.agents_by_role[filter_role]
        
        # Obtener tier para cada agente
        agent_tiers = {}
        for agent in agents_to_show:
            for tier, agents in self.tier_list.items():
                if agent in agents:
                    agent_tiers[agent] = tier
                    break
            if agent not in agent_tiers:
                agent_tiers[agent] = "No clasificado"
        
        # Ordenar agentes por tier y luego alfabéticamente
        tier_order = {"S-Tier": 0, "A-Tier": 1, "B-Tier": 2, "C-Tier": 3, "No clasificado": 4}
        agents_to_show.sort(key=lambda x: (tier_order.get(agent_tiers[x], 5), x))
        
        # Añadir agentes al grid
        row, col = 0, 0
        max_cols = 3  # Número de columnas en el grid
        
        for agent in agents_to_show:
            role = self.agent_roles[agent]
            tier = agent_tiers[agent]
            
            agent_card = AgentCard(agent, role, tier, self.agent_images.get(agent), size_factor=self.size_factor)
            agent_card.clicked.connect(self.on_agent_selected)
            agent_card.info_clicked.connect(self.show_agent_details)
            self.agent_cards[agent] = agent_card
            
            self.agent_grid.addWidget(agent_card, row, col)
            
            # Actualizar fila y columna
            col += 1
            if col >= max_cols:
                col = 0
                row += 1
    
    def filter_agents_by_role(self, role):
        """Filtrar agentes por rol"""
        self.populate_agents(role)
    
    def on_map_selected(self, map_name):
        """Manejar la selección de mapa"""
        # Desmarcar mapa anterior
        if self.selected_map and self.selected_map in self.map_cards:
            self.map_cards[self.selected_map].set_selected(False)
        
        # Marcar nuevo mapa
        self.selected_map = map_name
        self.map_cards[map_name].set_selected(True)
        
        # Actualizar etiqueta
        self.selected_map_label.setText(f"Mapa seleccionado: {map_name}")
        
        # Actualizar barra de estado
        self.statusBar().showMessage(f"Mapa seleccionado: {map_name}")
    
    def on_agent_selected(self, agent_name):
        """Manejar la selección de agente"""
        # Desmarcar agente anterior
        if self.selected_agent and self.selected_agent in self.agent_cards:
            self.agent_cards[self.selected_agent].set_selected(False)
        
        # Marcar nuevo agente
        self.selected_agent = agent_name
        self.agent_cards[agent_name].set_selected(True)
        
        # Actualizar etiqueta
        role = self.agent_roles.get(agent_name, "Desconocido")
        self.selected_agent_label.setText(f"Agente seleccionado: {agent_name} ({role})")
        
        # Actualizar barra de estado
        self.statusBar().showMessage(f"Agente seleccionado: {agent_name} ({role})")
    
    def on_style_changed(self, style):
        """Manejar el cambio de estilo de composición"""
        self.comp_style = style
        
        # Actualizar barra de estado
        self.statusBar().showMessage(f"Estilo de juego: {style}")
    
    def on_resize(self, event):
        """Manejar el evento de redimensionamiento de ventana"""
        # Calcular nuevo factor de tamaño basado en el ancho de la ventana
        width = event.size().width()
        
        if width < 1000:
            self.size_factor = 0.8
        elif width < 1200:
            self.size_factor = 0.9
        elif width < 1400:
            self.size_factor = 1.0
        elif width < 1600:
            self.size_factor = 1.1
        else:
            self.size_factor = 1.2
        
        # Actualizar tamaños de elementos
        self.update_element_sizes()
        
        # Llamar al método original
        super().resizeEvent(event)
    
    def update_element_sizes(self):
        """Actualizar tamaños de elementos según el factor de escala"""
        # Actualizar tarjetas de mapas
        for map_name, card in self.map_cards.items():
            card.set_size_factor(self.size_factor)
        
        # Actualizar tarjetas de agentes
        for agent_name, card in self.agent_cards.items():
            card.set_size_factor(self.size_factor)
    
    def show_welcome_message(self):
        """Mostrar mensaje de bienvenida en el panel de resultados"""
        # Limpiar contenido anterior
        self.clear_results()
        
        # Crear frame de bienvenida
        welcome_frame = QFrame()
        welcome_frame.setStyleSheet(f"background-color: {VALORANT_LIGHT_BLUE}; border-radius: 8px; padding: 20px;")
        welcome_layout = QVBoxLayout(welcome_frame)
        
        # Título de bienvenida
        welcome_title = QLabel("¡BIENVENIDO AL ASESOR DE COMPOSICIONES PREMIUM!")
        welcome_title.setStyleSheet(f"font-size: 20px; font-weight: bold; color: {VALORANT_RED};")
        welcome_title.setAlignment(Qt.AlignCenter)
        welcome_layout.addWidget(welcome_title)
        
        # Texto de bienvenida
        welcome_text = """
        Esta herramienta te ayudará a encontrar la composición de equipo ideal para cada mapa en Valorant.
        
        Para comenzar:
        1. Selecciona un mapa en el panel izquierdo
        2. Elige tu agente preferido
        3. Selecciona tu estilo de juego (Balanceado, Agresivo o Defensivo)
        4. Haz clic en "OBTENER COMPOSICIÓN"
        
        La herramienta generará una composición optimizada basada en la meta actual,
        adaptada a tus preferencias y al mapa seleccionado.
        
        Nuevas características en la versión Premium:
        • Información detallada de cada agente
        • Tier list actualizada
        • Recomendaciones personalizadas
        • Exportación de composiciones
        • Historial de composiciones
        • Interfaz responsiva y moderna
        """
        
        msg = QLabel(welcome_text)
        msg.setStyleSheet(f"font-size: 14px; color: {VALORANT_WHITE}; padding: 10px;")
        msg.setWordWrap(True)
        welcome_layout.addWidget(msg)
        
        # Botón para explorar agentes
        explore_button = HoverButton("EXPLORAR AGENTES")
        explore_button.clicked.connect(self.show_agent_browser)
        welcome_layout.addWidget(explore_button)
        
        # Añadir frame de bienvenida al contenido de resultados
        self.results_content_layout.addWidget(welcome_frame)
        
        # Añadir barra de progreso animada
        progress_frame = QFrame()
        progress_frame.setStyleSheet(f"background-color: {VALORANT_LIGHT_BLUE}; border-radius: 8px; padding: 10px; margin-top: 10px;")
        progress_layout = QVBoxLayout(progress_frame)
        
        loading_label = QLabel("Cargando datos de meta actualizados...")
        loading_label.setStyleSheet(f"font-size: 12px; color: {VALORANT_WHITE};")
        loading_label.setAlignment(Qt.AlignCenter)
        progress_layout.addWidget(loading_label)
        
        progress_bar = AnimatedProgressBar()
        progress_layout.addWidget(progress_bar)
        
        self.results_content_layout.addWidget(progress_frame)
        
        # Iniciar animación
        progress_bar.start_animation()
        
        # Simular carga completa después de 2 segundos
        QTimer.singleShot(2000, lambda: loading_label.setText("Datos de meta cargados correctamente"))
    
    def clear_results(self):
        """Limpiar el panel de resultados"""
        # Eliminar todos los widgets del layout de resultados
        while self.results_content_layout.count():
            item = self.results_content_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
    
    def generate_composition(self):
        """Generar y mostrar la composición del equipo"""
        if not self.selected_map:
            QMessageBox.warning(self, "Mapa no seleccionado", 
                              "Por favor, selecciona un mapa antes de generar la composición.")
            return
            
        if not self.selected_agent:
            QMessageBox.warning(self, "Agente no seleccionado", 
                              "Por favor, selecciona un agente que quieras jugar.")
            return
        
        # Mostrar barra de progreso mientras se genera la composición
        self.statusBar().showMessage("Generando composición...")
        
        # Limpiar resultados anteriores
        self.clear_results()
        
        # Añadir barra de progreso animada
        progress_frame = QFrame()
        progress_frame.setStyleSheet(f"background-color: {VALORANT_LIGHT_BLUE}; border-radius: 8px; padding: 10px;")
        progress_layout = QVBoxLayout(progress_frame)
        
        loading_label = QLabel("Generando composición óptima...")
        loading_label.setStyleSheet(f"font-size: 14px; color: {VALORANT_WHITE};")
        loading_label.setAlignment(Qt.AlignCenter)
        progress_layout.addWidget(loading_label)
        
        progress_bar = AnimatedProgressBar()
        progress_layout.addWidget(progress_bar)
        
        self.results_content_layout.addWidget(progress_frame)
        
        # Iniciar animación
        progress_bar.start_animation()
        
        # Simular procesamiento y mostrar resultados después de 1 segundo
        QTimer.singleShot(1000, self.show_composition_results)
    
    def show_composition_results(self):
        """Mostrar los resultados de la composición generada"""
        # Limpiar resultados anteriores
        self.clear_results()
        
        # Obtener la composición meta para el mapa seleccionado
        if self.comp_style == "Agresiva":
            base_comp = self.map_comps[self.selected_map]["aggressive"]
        elif self.comp_style == "Defensiva":
            base_comp = self.map_comps[self.selected_map]["defensive"]
        else:  # Balanceada (default)
            base_comp = self.map_comps[self.selected_map]["pro"]
        
        ranked_comp = self.map_comps[self.selected_map]["ranked"]
        alt_comp = self.map_comps[self.selected_map]["alt"]
        description = self.map_comps[self.selected_map]["description"]
        
        # Ajustar la composición según el agente preferido
        final_comp = self.adjust_composition(base_comp, ranked_comp, alt_comp, self.selected_agent)
        
        # Crear sección de mapa
        map_section = QFrame()
        map_section.setStyleSheet(f"background-color: {VALORANT_LIGHT_BLUE}; border-radius: 8px; padding: 15px;")
        map_layout = QVBoxLayout(map_section)
        
        # Cabecera con mapa y estilo
        header_frame = QFrame()
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(0, 0, 0, 0)
        
        # Imagen del mapa (si está disponible)
        if self.selected_map in self.map_images and self.map_images[self.selected_map]:
            map_img_label = QLabel()
            pixmap = QPixmap.fromImage(self.map_images[self.selected_map])
            pixmap = pixmap.scaled(200, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            map_img_label.setPixmap(pixmap)
            header_layout.addWidget(map_img_label)
        
        # Información del mapa
        map_info_frame = QFrame()
        map_info_layout = QVBoxLayout(map_info_frame)
        
        # Título del mapa
        map_title = QLabel(f"MAPA: {self.selected_map.upper()}")
        map_title.setStyleSheet(f"font-size: 20px; font-weight: bold; color: {VALORANT_RED};")
        map_info_layout.addWidget(map_title)
        
        # Estilo de composición
        style_label = QLabel(f"ESTILO: {self.comp_style.upper()}")
        style_label.setStyleSheet(f"font-size: 16px; font-weight: bold; color: {VALORANT_WHITE};")
        map_info_layout.addWidget(style_label)
        
        header_layout.addWidget(map_info_frame, 1)  # 1 = stretch factor
        map_layout.addWidget(header_frame)
        
        # Descripción del mapa
        desc_label = QLabel("ESTRATEGIA RECOMENDADA:")
        desc_label.setStyleSheet(f"font-size: 14px; font-weight: bold; color: {VALORANT_WHITE}; margin-top: 10px;")
        map_layout.addWidget(desc_label)
        
        desc_text = QLabel(description)
        desc_text.setStyleSheet(f"font-size: 12px; color: {VALORANT_WHITE};")
        desc_text.setWordWrap(True)
        map_layout.addWidget(desc_text)
        
        # Añadir sección de mapa al contenido de resultados
        self.results_content_layout.addWidget(map_section)
        
        # Crear sección de composición
        comp_section = QFrame()
        comp_section.setStyleSheet(f"background-color: {VALORANT_LIGHT_BLUE}; border-radius: 8px; padding: 15px;")
        comp_layout = QVBoxLayout(comp_section)
        
        # Título de composición
        comp_title = QLabel("COMPOSICIÓN DE EQUIPO")
        comp_title.setStyleSheet(f"font-size: 18px; font-weight: bold; color: {VALORANT_RED};")
        comp_layout.addWidget(comp_title)
        
        # Agrupar agentes por rol
        roles_used = {}
        for agent in final_comp:
            role = self.agent_roles[agent]
            if role not in roles_used:
                roles_used[role] = []
            roles_used[role].append(agent)
        
        # Mostrar agentes por rol
        role_order = ["Duelista", "Iniciador", "Controlador", "Centinela"]
        
        for role in role_order:
            if role in roles_used and roles_used[role]:
                # Crear frame para el rol
                role_frame = QFrame()
                role_frame.setStyleSheet("background-color: transparent;")
                role_layout = QVBoxLayout(role_frame)
                role_layout.setContentsMargins(0, 10, 0, 5)
                
                # Etiqueta de rol
                role_color = ROLE_COLORS.get(role, VALORANT_WHITE)
                
                role_label = QLabel(role.upper())
                role_label.setStyleSheet(f"font-size: 14px; font-weight: bold; color: {role_color};")
                role_layout.addWidget(role_label)
                
                # Frame para los agentes de este rol
                agents_frame = QFrame()
                agents_frame.setStyleSheet("background-color: transparent;")
                agents_layout = QHBoxLayout(agents_frame)
                agents_layout.setContentsMargins(0, 0, 0, 0)
                agents_layout.setSpacing(15)
                
                # Añadir cada agente
                for agent in roles_used[role]:
                    # Crear card para el agente
                    agent_role = self.agent_roles[agent]
                    agent_tier = self.get_agent_tier(agent)
                    
                    agent_card = AgentCard(agent, agent_role, agent_tier, self.agent_images.get(agent), size_factor=self.size_factor)
                    
                    # Marcar como preferido si es el agente seleccionado
                    if agent == self.selected_agent:
                        agent_card.set_preferred(True)
                    
                    # Conectar señal de info
                    agent_card.info_clicked.connect(self.show_agent_details)
                    
                    agents_layout.addWidget(agent_card)
                
                role_layout.addWidget(agents_frame)
                comp_layout.addWidget(role_frame)
        
        # Añadir sección de composición al contenido de resultados
        self.results_content_layout.addWidget(comp_section)
        
        # Crear sección de recomendaciones
        tips_section = QFrame()
        tips_section.setStyleSheet(f"background-color: {VALORANT_LIGHT_BLUE}; border-radius: 8px; padding: 15px;")
        tips_layout = QVBoxLayout(tips_section)
        
        # Título de recomendaciones
        tips_title = QLabel("RECOMENDACIONES ADICIONALES")
        tips_title.setStyleSheet(f"font-size: 16px; font-weight: bold; color: {VALORANT_RED};")
        tips_layout.addWidget(tips_title)
        
        # Generar consejos
        tips = self.generate_tips(self.selected_map, final_comp, self.selected_agent, self.comp_style)
        
        # Añadir cada consejo
        for tip in tips:
            tip_frame = QFrame()
            tip_frame.setStyleSheet("background-color: transparent;")
            tip_layout = QHBoxLayout(tip_frame)
            tip_layout.setContentsMargins(0, 5, 0, 5)
            
            # Bullet point
            bullet = QLabel("•")
            bullet.setStyleSheet(f"font-size: 16px; font-weight: bold; color: {VALORANT_RED};")
            tip_layout.addWidget(bullet)
            
            # Texto del consejo
            tip_text = QLabel(tip)
            tip_text.setStyleSheet(f"font-size: 12px; color: {VALORANT_WHITE};")
            tip_text.setWordWrap(True)
            tip_layout.addWidget(tip_text, 1)  # 1 = stretch factor
            
            tips_layout.addWidget(tip_frame)
        
        # Añadir sección de recomendaciones al contenido de resultados
        self.results_content_layout.addWidget(tips_section)
        
        # Crear sección de composiciones alternativas
        alt_section = QFrame()
        alt_section.setStyleSheet(f"background-color: {VALORANT_LIGHT_BLUE}; border-radius: 8px; padding: 15px;")
        alt_layout = QVBoxLayout(alt_section)
        
        # Título de composiciones alternativas
        alt_title = QLabel("COMPOSICIONES ALTERNATIVAS")
        alt_title.setStyleSheet(f"font-size: 16px; font-weight: bold; color: {VALORANT_RED};")
        alt_layout.addWidget(alt_title)
        
        # Composición Pro
        pro_label = QLabel("Composición Pro:")
        pro_label.setStyleSheet(f"font-size: 14px; font-weight: bold; color: {VALORANT_WHITE}; margin-top: 10px;")
        alt_layout.addWidget(pro_label)
        
        pro_text = QLabel(", ".join(self.map_comps[self.selected_map]["pro"]))
        pro_text.setStyleSheet(f"font-size: 12px; color: {VALORANT_WHITE};")
        pro_text.setWordWrap(True)
        alt_layout.addWidget(pro_text)
        
        # Composición Ranked
        ranked_label = QLabel("Composición Ranked:")
        ranked_label.setStyleSheet(f"font-size: 14px; font-weight: bold; color: {VALORANT_WHITE}; margin-top: 10px;")
        alt_layout.addWidget(ranked_label)
        
        ranked_text = QLabel(", ".join(ranked_comp))
        ranked_text.setStyleSheet(f"font-size: 12px; color: {VALORANT_WHITE};")
        ranked_text.setWordWrap(True)
        alt_layout.addWidget(ranked_text)
        
        # Composición Alt
        alt_comp_label = QLabel("Composición Alternativa:")
        alt_comp_label.setStyleSheet(f"font-size: 14px; font-weight: bold; color: {VALORANT_WHITE}; margin-top: 10px;")
        alt_layout.addWidget(alt_comp_label)
        
        alt_comp_text = QLabel(", ".join(alt_comp))
        alt_comp_text.setStyleSheet(f"font-size: 12px; color: {VALORANT_WHITE};")
        alt_comp_text.setWordWrap(True)
        alt_layout.addWidget(alt_comp_text)
        
        # Añadir sección de composiciones alternativas al contenido de resultados
        self.results_content_layout.addWidget(alt_section)
        
        # Botones de acción
        actions_frame = QFrame()
        actions_frame.setStyleSheet(f"background-color: {VALORANT_LIGHT_BLUE}; border-radius: 8px; padding: 15px;")
        actions_layout = QHBoxLayout(actions_frame)
        
        # Botón para guardar composición
        save_button = HoverButton("Guardar Composición")
        save_button.clicked.connect(self.save_composition)
        actions_layout.addWidget(save_button)
        
        # Botón para exportar composición
        export_button = HoverButton("Exportar Composición")
        export_button.clicked.connect(self.export_composition)
        actions_layout.addWidget(export_button)
        
        # Botón para ver detalles de agentes
        details_button = HoverButton("Ver Detalles de Agentes", color=VALORANT_LIGHT_BLUE)
        details_button.clicked.connect(self.show_agent_browser)
        actions_layout.addWidget(details_button)
        
        self.results_content_layout.addWidget(actions_frame)
        
        # Guardar la composición en el historial
        self.composition_history.append({
            "map": self.selected_map,
            "agent": self.selected_agent,
            "style": self.comp_style,
            "composition": final_comp
        })
        
        # Actualizar barra de estado
        self.statusBar().showMessage(f"Composición generada para {self.selected_map} con {self.selected_agent}")
    
    def adjust_composition(self, base_comp, ranked_comp, alt_comp, preferred_agent):
        """Ajustar la composición basada en el agente preferido"""
        # Si el agente preferido ya está en la composición base, no hay cambios
        if preferred_agent in base_comp:
            return base_comp.copy()
        
        # Encontrar el rol del agente preferido
        preferred_role = self.agent_roles[preferred_agent]
        
        # Intentar reemplazar un agente del mismo rol en la composición base
        final_comp = base_comp.copy()
        replaced = False
        
        for i, agent in enumerate(base_comp):
            if self.agent_roles.get(agent) == preferred_role:
                final_comp[i] = preferred_agent
                replaced = True
                break
        
        # Si no se pudo reemplazar por rol, buscar en otras composiciones
        if not replaced:
            # Verificar si el agente está en la composición ranked o alt
            if preferred_agent in ranked_comp:
                final_comp = ranked_comp.copy()
            elif preferred_agent in alt_comp:
                final_comp = alt_comp.copy()
            else:
                # Último recurso - reemplazar un agente menos importante
                # Identificar agentes core que aparecen en todas las composiciones
                core_agents = set(base_comp).intersection(set(ranked_comp)).intersection(set(alt_comp))
                non_core = [agent for agent in base_comp if agent not in core_agents]
                
                if non_core:
                    # Reemplazar un agente no core
                    replace_idx = base_comp.index(random.choice(non_core))
                else:
                    # Si todos son core, reemplazar uno al azar pero no un controlador
                    controllers = [i for i, agent in enumerate(base_comp) 
                                 if self.agent_roles.get(agent) == "Controlador"]
                    
                    # Evitar reemplazar controladores si es posible
                    non_controllers = [i for i in range(len(base_comp)) if i not in controllers]
                    
                    if non_controllers and preferred_role != "Controlador":
                        replace_idx = random.choice(non_controllers)
                    else:
                        replace_idx = random.randint(0, len(base_comp) - 1)
                
                final_comp[replace_idx] = preferred_agent
        
        # Asegurar que la composición tenga al menos un controlador
        has_controller = any(self.agent_roles.get(agent) == "Controlador" for agent in final_comp)
        
        if not has_controller:
            # Buscar un agente que no sea el preferido para reemplazar
            for i, agent in enumerate(final_comp):
                if agent != preferred_agent and self.agent_roles.get(agent) != "Controlador":
                    # Reemplazar con un controlador popular
                    final_comp[i] = "Omen"  # Controlador versátil para la mayoría de mapas
                    break
        
        return final_comp
    
    def generate_tips(self, map_name, composition, preferred_agent, comp_style):
        """Generar consejos específicos para el mapa y la composición"""
        tips = []
        
        # Añadir consejos específicos del mapa
        if map_name == "Ascent":
            tips.append("Utiliza habilidades de reconocimiento para controlar Mid y asegurar la transición entre sitios.")
            tips.append("Mantén control de Catwalk y Market con tus controladores para ejecutar rápidamente en A o B.")
            if comp_style == "Agresiva":
                tips.append("Aprovecha las entradas rápidas por A Main y B Main con duelistas para sorprender a los defensores.")
            elif comp_style == "Defensiva":
                tips.append("Establece una defensa fuerte en Heaven y CT para controlar múltiples ángulos.")
        elif map_name == "Bind":
            tips.append("Utiliza los teletransportadores para rotaciones rápidas y flanqueos sorpresa.")
            tips.append("Coordina utilidad para limpiar esquinas en Hookah y Showers.")
            if comp_style == "Agresiva":
                tips.append("Presiona agresivamente Hookah y Showers para tomar control temprano del mapa.")
            elif comp_style == "Defensiva":
                tips.append("Coloca centinelas en los teletransportadores para detectar rotaciones enemigas.")
        elif map_name == "Breeze":
            tips.append("La Pantalla Tóxica de Viper es esencial para dividir los amplios espacios abiertos.")
            tips.append("Utiliza operadores en las largas líneas de visión de A Main y Mid.")
            if comp_style == "Agresiva":
                tips.append("Toma control agresivo de Cave y Nest para presionar a los defensores desde múltiples ángulos.")
            elif comp_style == "Defensiva":
                tips.append("Mantén operadores en A Bridge y B Nest para controlar las líneas largas.")
        elif map_name == "Fracture":
            tips.append("Coordina ataques desde ambos lados del mapa para dividir atención de defensores.")
            tips.append("Prioriza el control de Dish y Arcade para facilitar rotaciones a ambos sitios.")
            if comp_style == "Agresiva":
                tips.append("Utiliza a Breach y Fade para entradas coordinadas desde ambos lados del sitio.")
            elif comp_style == "Defensiva":
                tips.append("Coloca centinelas en puntos clave como Dish y Tower para detectar flancos.")
        elif map_name == "Haven":
            tips.append("Coordina tácticas para manejar los tres sitios de bomba y sus múltiples entradas.")
            tips.append("Divide habilidades defensivas eficientemente entre todos los sitios.")
            if comp_style == "Agresiva":
                tips.append("Presiona agresivamente C Long o A Long para forzar rotaciones y crear espacio.")
            elif comp_style == "Defensiva":
                tips.append("Mantén control de Garage para facilitar rotaciones rápidas entre sitios.")
        elif map_name == "Icebox":
            tips.append("La Pantalla Tóxica de Viper es crucial para dividir sitios y crear espacio para plantar.")
            tips.append("Utiliza el muro de Sage para facilitar plantaciones seguras en sitios abiertos como B.")
            if comp_style == "Agresiva":
                tips.append("Aprovecha el movimiento vertical en B Site para sorprender a los defensores.")
            elif comp_style == "Defensiva":
                tips.append("Coloca utilidad de Killjoy en B para retrasar pushes y facilitar retakes.")
        elif map_name == "Lotus":
            tips.append("Aprovecha las puertas rotatorias para ejecutar rotaciones silenciosas.")
            tips.append("Mantén control de Main Hall para dividir el mapa y facilitar rotaciones.")
            if comp_style == "Agresiva":
                tips.append("Utiliza a Raze para limpiar espacios cerrados cerca de las puertas rotatorias.")
            elif comp_style == "Defensiva":
                tips.append("Coloca centinelas en C Mound y A Tree para detectar flancos a través de las puertas.")
        elif map_name == "Pearl":
            tips.append("Usa controladores para bloquear líneas de visión largas en Mid y A Main.")
            tips.append("Controla Water para poder flanquear B desde múltiples ángulos.")
            if comp_style == "Agresiva":
                tips.append("Presiona agresivamente Mid para dividir el mapa y controlar rotaciones.")
            elif comp_style == "Defensiva":
                tips.append("Mantén control de Art y Link para facilitar rotaciones defensivas.")
        elif map_name == "Split":
            tips.append("Coordina habilidades para tomar control de Mid y presionar ambos sitios.")
            tips.append("Usa muros y humos para bloquear las visiones extensas de Heaven y Rafters.")
            if comp_style == "Agresiva":
                tips.append("Utiliza a Raze para entradas verticales sorpresa en A o B Main.")
            elif comp_style == "Defensiva":
                tips.append("Coloca centinelas en Mid Mail y Vents para detectar flancos.")
        elif map_name == "Sunset":
            tips.append("Aprovecha los múltiples niveles y ángulos verticales para sorprender a los enemigos.")
            tips.append("Coordina utilidad para limpiar espacios cerrados y esquinas.")
            if comp_style == "Agresiva":
                tips.append("Utiliza a Raze y Phoenix para limpiar espacios cerrados con su utilidad.")
            elif comp_style == "Defensiva":
                tips.append("Coloca a Deadlock y Killjoy para controlar áreas clave y retrasar pushes.")
        
        # Añadir consejos específicos de la composición
        duelist_count = sum(1 for agent in composition if self.agent_roles.get(agent) == "Duelista")
        controller_count = sum(1 for agent in composition if self.agent_roles.get(agent) == "Controlador")
        sentinel_count = sum(1 for agent in composition if self.agent_roles.get(agent) == "Centinela")
        initiator_count = sum(1 for agent in composition if self.agent_roles.get(agent) == "Iniciador")
        
        if duelist_count > 1:
            tips.append("Con múltiples duelistas, coordina las entradas para no desperdiciar utilidad ni arriesgar demasiado.")
        
        if controller_count > 1:
            tips.append("Distribuye los humos entre sitios para maximizar la cobertura y duración.")
        
        if "Jett" in composition:
            tips.append("Utiliza a Jett para tomar ángulos agresivos con Operator y crear espacio para el equipo.")
        
        if "Viper" in composition:
            tips.append("Aprende los lineups de Viper para pantallas toxicas y hoyos venenosos clave.")
        
        if "Omen" in composition:
            tips.append("Aprovecha la teletransportación de Omen para flanqueos sorpresa o reposicionamientos.")
        
        if "Sova" in composition:
            tips.append("Comunica la información obtenida con las flechas de reconocimiento de Sova.")
        
        if "Killjoy" in composition:
            tips.append("Coloca utilidad de Killjoy en ángulos sorpresa o para defender post-planta.")
        
        if "Sage" in composition and map_name in ["Split", "Icebox"]:
            tips.append("Usa el muro de Sage para bloquear entradas clave o facilitar plantaciones.")
        
        # Añadir consejos del agente preferido
        if preferred_agent == "Jett":
            tips.append("Como Jett, usa tus Cloudburst para cubrir ángulos mientras entras con Tailwind.")
        elif preferred_agent == "Raze":
            tips.append("Usa los Blast Pack de Raze para movimientos verticales sorpresa y entrada rápida.")
        elif preferred_agent == "Omen":
            tips.append("Coloca humos profundos para bloquear visión de Defenders mientras tu equipo toma espacio.")
        elif preferred_agent == "Viper":
            tips.append("Aprende los lineups post-planta de Viper para Snake Bite en ubicaciones comunes de defuse.")
        elif preferred_agent == "Sova":
            tips.append("Domina los rebotes de flecha y lugares de Drone para maximizar la información obtenida.")
        elif preferred_agent == "Killjoy":
            tips.append("Coloca Alarmbots en ubicaciones inesperadas para detectar flancos o pushes rápidos.")
        elif preferred_agent == "Cypher":
            tips.append("Usa la cámara de Cypher para vigilar flancos mientras el equipo ataca un sitio.")
        elif preferred_agent == "Breach":
            tips.append("Coordina tus flashes y aturdimientos con las entradas de los duelistas del equipo.")
        
        # Limitar a 6 consejos máximo
        return tips[:6]
    
    def get_agent_tier(self, agent):
        """Obtener el tier de un agente"""
        for tier, agents in self.tier_list.items():
            if agent in agents:
                return tier
        return "No clasificado"
    
    def show_agent_details(self, agent_name):
        """Mostrar detalles del agente en una ventana emergente"""
        agent_data = self.agent_details.get(agent_name, {})
        agent_image = self.agent_images.get(agent_name)
        
        dialog = AgentInfoDialog(agent_name, agent_data, agent_image, self)
        dialog.exec_()
    
    def show_agent_browser(self):
        """Mostrar explorador de agentes"""
        dialog = AgentBrowserDialog(self.agent_details, self.agent_images, self)
        dialog.exec_()
    
    def save_composition(self):
        """Guardar la composición actual en un archivo"""
        if not self.composition_history:
            QMessageBox.information(self, "Sin composición", 
                                  "No hay composición para guardar. Genera una composición primero.")
            return
        
        try:
            # Obtener la última composición
            last_comp = self.composition_history[-1]
            
            # Crear directorio de guardado si no existe
            save_dir = "composiciones"
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)
            
            # Solicitar ubicación de guardado
            filename, _ = QFileDialog.getSaveFileName(
                self, 
                "Guardar Composición",
                os.path.join(save_dir, f"{last_comp['map']}_{last_comp['agent']}_{last_comp['style']}.json"),
                "Archivos JSON (*.json)"
            )
            
            if not filename:
                return  # Usuario canceló
            
            # Guardar como JSON
            with open(filename, 'w') as f:
                json.dump(last_comp, f, indent=4)
            
            QMessageBox.information(self, "Composición guardada", 
                                  f"Composición guardada exitosamente en:\n{filename}")
        except Exception as e:
            QMessageBox.critical(self, "Error al guardar", 
                               f"No se pudo guardar la composición:\n{str(e)}")
    
    def show_help(self):
        """Mostrar ventana de ayuda"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Ayuda - Valorant Team Comp Advisor Premium")
        dialog.setMinimumSize(700, 500)
        dialog.setStyleSheet(f"""
            QDialog {{
                background-color: {VALORANT_BLUE};
            }}
            QLabel {{
                color: {VALORANT_WHITE};
            }}
            QTabWidget::pane {{
                border: 1px solid #2A3441;
                background-color: {VALORANT_LIGHT_BLUE};
                border-radius: 8px;
            }}
            QTabBar::tab {{
                background-color: {VALORANT_LIGHT_BLUE};
                color: {VALORANT_WHITE};
                border: 1px solid #2A3441;
                border-bottom: none;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                padding: 8px 12px;
                margin-right: 2px;
            }}
            QTabBar::tab:selected {{
                background-color: {VALORANT_RED};
                color: white;
            }}
            QTabBar::tab:!selected {{
                margin-top: 2px;
            }}
        """)
        
        # Layout
        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Título
        title_label = QLabel("GUÍA DE USO")
        title_label.setStyleSheet(f"font-size: 24px; font-weight: bold; color: {VALORANT_RED};")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # Tabs para organizar la ayuda
        tab_widget = QTabWidget()
        layout.addWidget(tab_widget)
        
        # Tab de uso básico
        basic_tab = QWidget()
        basic_layout = QVBoxLayout(basic_tab)
        
        basic_text = """
<h3>Cómo usar la aplicación</h3>
<ol>
    <li>Selecciona un mapa en el panel izquierdo.</li>
    <li>Elige tu agente preferido.</li>
    <li>Selecciona tu estilo de juego (Balanceado, Agresivo o Defensivo).</li>
    <li>Haz clic en "OBTENER COMPOSICIÓN".</li>
    <li>Revisa la composición recomendada y los consejos en el panel derecho.</li>
    <li>Opcionalmente, guarda la composición para referencia futura.</li>
</ol>

<h3>Entendiendo las recomendaciones</h3>
<ul>
    <li><b>Composición Pro:</b> Utilizada por equipos profesionales en torneos.</li>
    <li><b>Composición Ranked:</b> Optimizada para juego competitivo de alto nivel.</li>
    <li><b>Composición Alternativa:</b> Variación viable para diferentes estilos de juego.</li>
    <li><b>Composición Agresiva:</b> Enfocada en entradas rápidas y control de mapa.</li>
    <li><b>Composición Defensiva:</b> Prioriza control de sitios y retakes efectivos.</li>
</ul>

<p>El sistema intentará incluir tu agente preferido en la composición, reemplazando inteligentemente otro agente del mismo rol o ajustando la composición para mantener el balance.</p>
        """
        
        basic_info = QLabel(basic_text)
        basic_info.setTextFormat(Qt.RichText)
        basic_info.setWordWrap(True)
        basic_info.setOpenExternalLinks(True)
        basic_layout.addWidget(basic_info)
        
        tab_widget.addTab(basic_tab, "Uso Básico")
        
        # Tab de roles y tiers
        roles_tab = QWidget()
        roles_layout = QVBoxLayout(roles_tab)
        
        roles_text = """
<h3>Roles de agentes</h3>
<ul>
    <li><b>Duelistas:</b> Especialistas en entradas y tomar duelos. Crean espacio para el equipo.</li>
    <li><b>Iniciadores:</b> Proporcionan información y apoyo para entradas con flashes y reconocimiento.</li>
    <li><b>Controladores:</b> Controlan áreas con humos y habilidades de negación de espacio.</li>
    <li><b>Centinelas:</b> Especialistas defensivos que vigilan flancos y aseguran sitios.</li>
</ul>

<h3>Sistema de Tiers</h3>
<ul>
    <li><b>S-Tier:</b> Agentes meta dominantes, extremadamente efectivos en el parche actual.</li>
    <li><b>A-Tier:</b> Agentes muy fuertes y versátiles en la mayoría de mapas y composiciones.</li>
    <li><b>B-Tier:</b> Agentes sólidos pero situacionales o que requieren mayor coordinación.</li>
    <li><b>C-Tier:</b> Agentes que actualmente están en desventaja en la meta o requieren buffs.</li>
</ul>
        """
        
        roles_info = QLabel(roles_text)
        roles_info.setTextFormat(Qt.RichText)
        roles_info.setWordWrap(True)
        roles_layout.addWidget(roles_info)
        
        tab_widget.addTab(roles_tab, "Roles y Tiers")
        
        # Tab de consejos
        tips_tab = QWidget()
        tips_layout = QVBoxLayout(tips_tab)
        
        tips_text = """
<h3>Consejos para composiciones efectivas</h3>
<ul>
    <li>Asegúrate de tener al menos un controlador en tu equipo para humos y control de espacio.</li>
    <li>Balancear roles es importante: 1-2 duelistas, 1-2 iniciadores, 1 controlador, 1 centinela.</li>
    <li>Adapta tu composición al mapa: algunos agentes son más efectivos en ciertos mapas.</li>
    <li>Considera el estilo de juego de tu equipo al elegir la composición.</li>
    <li>Comunica y coordina utilidades con tu equipo para maximizar su efectividad.</li>
    <li>Aprende lineups y setups específicos para cada mapa con tus agentes principales.</li>
</ul>

<h3>Mapas y estrategias</h3>
<p>Cada mapa tiene características únicas que favorecen ciertos agentes y estrategias:</p>
<ul>
    <li><b>Mapas abiertos (Breeze, Icebox):</b> Viper es casi imprescindible para dividir espacios.</li>
    <li><b>Mapas con múltiples sitios (Haven):</b> Se requieren agentes con buena movilidad y control de flancos.</li>
    <li><b>Mapas con espacios cerrados (Split, Bind):</b> Raze y otros agentes con daño por área son muy efectivos.</li>
    <li><b>Mapas con verticales (Fracture, Sunset):</b> Agentes con movilidad vertical como Jett o Raze tienen ventaja.</li>
</ul>
        """
        
        tips_info = QLabel(tips_text)
        tips_info.setTextFormat(Qt.RichText)
        tips_info.setWordWrap(True)
        tips_layout.addWidget(tips_info)
        
        tab_widget.addTab(tips_tab, "Consejos")
        
        # Tab de funciones premium
        premium_tab = QWidget()
        premium_layout = QVBoxLayout(premium_tab)
        
        premium_text = """
<h3>Funciones Premium</h3>
<ul>
    <li><b>Explorador de Agentes:</b> Accede a información detallada de todos los agentes, incluyendo habilidades, estrategias y estadísticas.</li>
    <li><b>Tier List:</b> Consulta la tier list actualizada con los agentes más efectivos en la meta actual.</li>
    <li><b>Composiciones Pro:</b> Acceso a composiciones utilizadas por equipos profesionales en torneos.</li>
    <li><b>Recomendaciones Avanzadas:</b> Consejos específicos para cada mapa y composición, adaptados a tu estilo de juego.</li>
    <li><b>Exportar Composición:</b> Guarda y exporta tus composiciones en formato JSON para compartir con amigos.</li>
    <li><b>Historial de Composiciones:</b> Guarda y revisa el historial de composiciones generadas.</li>
    <li><b>Actualizaciones Futuras:</b> Acceso a nuevas funciones y mejoras en la aplicación.</li>
    
</ul>
<p>Estas funciones están diseñadas para mejorar tu experiencia
y ayudarte a dominar el juego.</p>
        """
        
        premium_info = QLabel(premium_text)
        premium_info.setTextFormat(Qt.RichText)
        premium_info.setWordWrap(True)
        premium_layout.addWidget(premium_info)
        
        tab_widget.addTab(premium_tab, "Funciones Premium")
        
        # Botón de cerrar
        close_button = QPushButton("Cerrar")
        close_button.setStyleSheet(f"background-color: {VALORANT_RED}; color: white; padding: 10px; border-radius: 5px;")
        close_button.clicked.connect(dialog.close)
        layout.addWidget(close_button, alignment=Qt.AlignRight)
        
        dialog.exec_()
        # Ajustar el tamaño de la ventana de ayuda
        dialog.resize(700, 500)
        dialog.setMinimumSize(700, 500)
        dialog.setMaximumSize(700, 500)
        dialog.setWindowModality(Qt.ApplicationModal)
        dialog.setAttribute(Qt.WA_DeleteOnClose, True)
        dialog.setWindowFlags(Qt.Window | Qt.WindowTitleHint | Qt.CustomizeWindowHint)
        dialog.setWindowIcon(QIcon("icon.png"))
        dialog.setWindowTitle("Ayuda - Valorant Team Comp Advisor Premium")
        dialog.setStyleSheet(f"background-color: {VALORANT_BLUE}; color: {VALORANT_WHITE};")
        dialog.setContentsMargins(20, 20, 20, 20)
        dialog.setLayout(layout)

    def show_about(self):
        """Mostrar información acerca de la aplicación"""
        QMessageBox.about(self, "Acerca de", 
                        "Valorant Team Comp Advisor Premium v3.0\n\n"
                        "Desarrollado para ayudar a los jugadores de Valorant a crear composiciones óptimas.\n\n"
                        "Datos actualizados a mayo 2025.\n\n"
                        "© 2025 Todos los derechos reservados.")
    
    def show_history(self):
        """Mostrar historial de composiciones"""
        if not self.composition_history:
            QMessageBox.information(self, "Historial vacío", 
                                  "No hay composiciones en el historial. Genera una composición primero.")
            return
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Historial de Composiciones")
        dialog.setMinimumSize(600, 400)
        dialog.setStyleSheet(f"""
            QDialog {{
                background-color: {VALORANT_BLUE};
            }}
            QLabel {{
                color: {VALORANT_WHITE};
            }}
            QTableWidget {{
                background-color: {VALORANT_LIGHT_BLUE};
                color: {VALORANT_WHITE};
                gridline-color: #2A3441;
                border: none;
            }}
            QTableWidget::item {{
                padding: 5px;
            }}
            QTableWidget::item:selected {{
                background-color: {VALORANT_RED};
            }}
            QHeaderView::section {{
                background-color: {VALORANT_RED};
                color: {VALORANT_WHITE};
                padding: 5px;
                border: none;
            }}
        """)
        
        # Layout
        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Título
        title_label = QLabel("HISTORIAL DE COMPOSICIONES")
        title_label.setStyleSheet(f"font-size: 18px; font-weight: bold; color: {VALORANT_RED};")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # Tabla de historial
        table = QTableWidget()
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(["Mapa", "Agente", "Estilo", "Composición"])
        table.horizontalHeader().setStretchLastSection(True)
        table.setEditTriggers(QTableWidget.NoEditTriggers)
        table.setSelectionBehavior(QTableWidget.SelectRows)
        table.setSelectionMode(QTableWidget.SingleSelection)
        
        # Añadir filas
        table.setRowCount(len(self.composition_history))
        for i, comp in enumerate(reversed(self.composition_history)):
            table.setItem(i, 0, QTableWidgetItem(comp["map"]))
            table.setItem(i, 1, QTableWidgetItem(comp["agent"]))
            table.setItem(i, 2, QTableWidgetItem(comp["style"]))
            table.setItem(i, 3, QTableWidgetItem(", ".join(comp["composition"])))
        
        # Ajustar tamaño de columnas
        table.resizeColumnsToContents()
        
        layout.addWidget(table)
        
        # Botones de acción
        button_layout = QHBoxLayout()
        
        # Botón para cargar composición
        load_button = HoverButton("Cargar Composición")
        load_button.clicked.connect(lambda: self.load_composition_from_history(table.currentRow()))
        button_layout.addWidget(load_button)
        
        # Botón para exportar composición
        export_button = HoverButton("Exportar Composición")
        export_button.clicked.connect(lambda: self.export_composition_from_history(table.currentRow()))
        button_layout.addWidget(export_button)
        
        # Botón para cerrar
        close_button = HoverButton("Cerrar", color=VALORANT_LIGHT_BLUE)
        close_button.clicked.connect(dialog.close)
        button_layout.addWidget(close_button)
        
        layout.addLayout(button_layout)
        
        dialog.exec_()
    
    def load_composition_from_history(self, row):
        """Cargar una composición desde el historial"""
        if row < 0 or row >= len(self.composition_history):
            QMessageBox.warning(self, "Selección inválida", 
                              "Por favor, selecciona una composición del historial.")
            return
        
        # Obtener la composición seleccionada (en orden inverso)
        comp = self.composition_history[len(self.composition_history) - 1 - row]
        
        # Seleccionar el mapa
        if comp["map"] in self.map_cards:
            self.on_map_selected(comp["map"])
        
        # Seleccionar el agente
        if comp["agent"] in self.agent_cards:
            self.on_agent_selected(comp["agent"])
        
        # Seleccionar el estilo
        for radio in self.style_group.buttons():
            if radio.text() == comp["style"]:
                radio.setChecked(True)
                self.comp_style = comp["style"]
                break
        
        # Mostrar la composición
        self.show_composition_results()
    
    def export_composition(self):
        """Exportar la composición actual"""
        if not self.composition_history:
            QMessageBox.information(self, "Sin composición", 
                                  "No hay composición para exportar. Genera una composición primero.")
            return
        
        # Obtener la última composición
        last_comp = self.composition_history[-1]
        
        # Crear directorio de exportación si no existe
        export_dir = "exportaciones"
        if not os.path.exists(export_dir):
            os.makedirs(export_dir)
        
        # Solicitar ubicación de guardado
        filename, _ = QFileDialog.getSaveFileName(
            self, 
            "Exportar Composición",
            os.path.join(export_dir, f"{last_comp['map']}_{last_comp['agent']}_{last_comp['style']}.json"),
            "Archivos JSON (*.json)"
        )
        
        if not filename:
            return  # Usuario canceló
        
        try:
            # Crear datos de exportación
            export_data = {
                "map": last_comp["map"],
                "agent": last_comp["agent"],
                "style": last_comp["style"],
                "composition": last_comp["composition"],
                "timestamp": "Mayo 2025",
                "app_version": "3.0"
            }
            
            # Guardar como JSON
            with open(filename, 'w') as f:
                json.dump(export_data, f, indent=4)
            
            QMessageBox.information(self, "Composición exportada", 
                                  f"Composición exportada exitosamente en:\n{filename}")
        except Exception as e:
            QMessageBox.critical(self, "Error al exportar", 
                               f"No se pudo exportar la composición:\n{str(e)}")
    
    def export_composition_from_history(self, row):
        """Exportar una composición desde el historial"""
        if row < 0 or row >= len(self.composition_history):
            QMessageBox.warning(self, "Selección inválida", 
                              "Por favor, selecciona una composición del historial.")
            return
        
        # Obtener la composición seleccionada (en orden inverso)
        comp = self.composition_history[len(self.composition_history) - 1 - row]
        
        # Crear directorio de exportación si no existe
        export_dir = "exportaciones"
        if not os.path.exists(export_dir):
            os.makedirs(export_dir)
        
        # Solicitar ubicación de guardado
        filename, _ = QFileDialog.getSaveFileName(
            self, 
            "Exportar Composición",
            os.path.join(export_dir, f"{comp['map']}_{comp['agent']}_{comp['style']}.json"),
            "Archivos JSON (*.json)"
        )
        
        if not filename:
            return  # Usuario canceló
        
        try:
            # Crear datos de exportación
            export_data = {
                "map": comp["map"],
                "agent": comp["agent"],
                "style": comp["style"],
                "composition": comp["composition"],
                "timestamp": "Mayo 2025",
                "app_version": "3.0"
            }
            
            # Guardar como JSON
            with open(filename, 'w') as f:
                json.dump(export_data, f, indent=4)
            
            QMessageBox.information(self, "Composición exportada", 
                                  f"Composición exportada exitosamente en:\n{filename}")
        except Exception as e:
            QMessageBox.critical(self, "Error al exportar", 
                               f"No se pudo exportar la composición:\n{str(e)}")

# Función principal para iniciar la aplicación
def main():
    app = QApplication(sys.argv)
    window = ValorantTeamCompAdvisor()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
        