import streamlit as st
import numpy as np
import time
import random
import math
from streamlit.components.v1 import html

# Page config must be first
st.set_page_config(
    page_title="Ultimate Tic-Tac-Toe - AI Champion",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Add Font Awesome and other icon libraries
st.markdown("""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css">
<link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
""", unsafe_allow_html=True)

# Custom CSS for modern, fancy styling
st.markdown("""
<style>
    /* Modern gradient background */
    .stApp {
        background: radial-gradient(circle at 20% 50%, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        color: white;
    }
    
    /* Animated title with neon effect */
    @keyframes neonPulse {
        0% { text-shadow: 0 0 10px #00fff9, 0 0 20px #00fff9, 0 0 30px #00fff9; }
        50% { text-shadow: 0 0 20px #ff00e5, 0 0 30px #ff00e5, 0 0 40px #ff00e5; }
        100% { text-shadow: 0 0 10px #00fff9, 0 0 20px #00fff9, 0 0 30px #00fff9; }
    }
    
    .neon-title {
        font-size: 3.5rem;
        font-weight: 900;
        text-align: center;
        animation: neonPulse 3s infinite;
        margin-bottom: 0.5rem;
        letter-spacing: 4px;
    }
    
    .neon-title i {
        margin: 0 10px;
        color: #fff;
    }
    
    /* Glass card effect */
    .glass-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        border: 1px solid rgba(255, 255, 255, 0.18);
        margin: 1rem 0;
        transition: transform 0.3s ease;
    }
    
    .glass-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 48px 0 rgba(31, 38, 135, 0.5);
    }
    
    /* Animated status box */
    @keyframes slideIn {
        from { transform: translateX(-100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    .status-neon {
        padding: 1.2rem;
        border-radius: 15px;
        text-align: center;
        font-size: 1.4rem;
        font-weight: 700;
        animation: slideIn 0.5s ease;
        box-shadow: 0 0 20px rgba(0,0,0,0.3);
        margin-bottom: 1.5rem;
    }
    
    /* X and O icons with animations */
    @keyframes popIn {
        0% { transform: scale(0) rotate(-180deg); opacity: 0; }
        100% { transform: scale(1) rotate(0); opacity: 1; }
    }
    
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0px); }
    }
    
    .x-icon {
        color: #ff4757;
        font-size: 4rem;
        animation: popIn 0.3s ease, float 3s infinite;
        text-shadow: 0 0 20px #ff4757;
    }
    
    .o-icon {
        color: #1e90ff;
        font-size: 4rem;
        animation: popIn 0.3s ease, float 3s infinite 0.5s;
        text-shadow: 0 0 20px #1e90ff;
    }
    
    .empty-cell {
        background: rgba(255, 255, 255, 0.03);
        border: 2px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .empty-cell:hover {
        background: rgba(255, 255, 255, 0.1);
        border-color: rgba(255, 255, 255, 0.3);
        transform: scale(1.05);
        box-shadow: 0 0 30px rgba(255,255,255,0.2);
    }
    
    /* Animated buttons */
    .fancy-button {
        background: linear-gradient(45deg, #667eea, #764ba2);
        border: none;
        padding: 0.8rem 2rem;
        border-radius: 50px;
        color: white;
        font-weight: 600;
        font-size: 1.1rem;
        cursor: pointer;
        transition: all 0.3s ease;
        width: 100%;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .fancy-button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6);
    }
    
    .fancy-button i {
        margin-right: 10px;
    }
    
    /* Stats cards */
    .stat-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        backdrop-filter: blur(5px);
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    .stat-card i {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
        color: #fff;
    }
    
    /* Winning line effect */
    @keyframes winGlow {
        0% { border-color: #ffd700; box-shadow: 0 0 10px #ffd700; }
        50% { border-color: #ffa500; box-shadow: 0 0 20px #ffa500; }
        100% { border-color: #ffd700; box-shadow: 0 0 10px #ffd700; }
    }
    
    .winning-cell {
        animation: winGlow 1.5s infinite;
        border: 3px solid #ffd700;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .neon-title { font-size: 2rem; }
        .x-icon, .o-icon { font-size: 2.5rem; }
        .status-neon { font-size: 1rem; }
    }
    
    /* Floating particles */
    .particle {
        position: fixed;
        pointer-events: none;
        opacity: 0.3;
        z-index: -1;
    }
</style>
""", unsafe_allow_html=True)

# Floating particles animation
particles_html = """
<div style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: -1; overflow: hidden;">
    <i class="fas fa-circle particle" style="top: 10%; left: 5%; color: #ff6b6b; font-size: 20px; animation: float 20s infinite;"></i>
    <i class="fas fa-circle particle" style="top: 70%; left: 90%; color: #4ecdc4; font-size: 15px; animation: float 25s infinite;"></i>
    <i class="fas fa-square particle" style="top: 40%; left: 80%; color: #ffeaa7; font-size: 12px; animation: float 18s infinite;"></i>
    <i class="fas fa-circle particle" style="top: 80%; left: 30%; color: #a8e6cf; font-size: 25px; animation: float 22s infinite;"></i>
    <i class="fas fa-triangle particle" style="top: 20%; left: 70%; color: #ff8c5a; font-size: 18px; animation: float 30s infinite;"></i>
</div>
"""
html(particles_html)

# Initialize session state
def init_session_state():
    defaults = {
        'board': np.zeros((3, 3), dtype=int),
        'game_over': False,
        'player': 1,
        'winning_line': None,
        'last_move': None,
        'animation_frame': 0,
        'ai_thinking': False,
        'winner': 0,
        'win_sound_played': False,
        'human_score': 0,
        'ai_score': 0,
        'draw_score': 0
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()

# Title with Font Awesome icons
st.markdown("""
<div style="text-align: center; margin-top: 1rem; margin-bottom: 2rem;">
    <h1 class="neon-title">
        <i class="fas fa-robot"></i> 
        ULTIMATE TIC-TAC-TOE 
        <i class="fas fa-crown"></i>
    </h1>
    <p style="color: #a8dadc; font-size: 1.2rem;">
        <i class="fas fa-user"></i> Human <span style="color: #ff4757;">❌</span> 
        VS 
        <i class="fas fa-microchip"></i> AI <span style="color: #1e90ff;">◯</span>
        <br>
        <small style="color: #b2bec3;"><i class="fas fa-brain"></i> Powered by Minimax Algorithm</small>
    </p>
</div>
""", unsafe_allow_html=True)

# Game functions
def check_winner(board):
    """Check winner and return winning line"""
    # Rows
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != 0:
            return board[i][0], [(i, 0), (i, 2)]
    
    # Columns
    for j in range(3):
        if board[0][j] == board[1][j] == board[2][j] != 0:
            return board[0][j], [(0, j), (2, j)]
    
    # Diagonals
    if board[0][0] == board[1][1] == board[2][2] != 0:
        return board[0][0], [(0, 0), (2, 2)]
    if board[0][2] == board[1][1] == board[2][0] != 0:
        return board[0][2], [(0, 2), (2, 0)]
    
    return 0, None

def is_board_full(board):
    return not np.any(board == 0)

def minimax(board, depth, is_maximizing):
    winner, _ = check_winner(board)
    
    if winner == 2:
        return 10 - depth
    elif winner == 1:
        return depth - 10
    elif is_board_full(board):
        return 0
    
    if is_maximizing:
        best_score = -float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == 0:
                    board[i][j] = 2
                    score = minimax(board, depth + 1, False)
                    board[i][j] = 0
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == 0:
                    board[i][j] = 1
                    score = minimax(board, depth + 1, True)
                    board[i][j] = 0
                    best_score = min(score, best_score)
        return best_score

def ai_move():
    best_score = -float('inf')
    best_move = None
    
    for i in range(3):
        for j in range(3):
            if st.session_state.board[i][j] == 0:
                st.session_state.board[i][j] = 2
                score = minimax(st.session_state.board, 0, False)
                st.session_state.board[i][j] = 0
                
                if score > best_score:
                    best_score = score
                    best_move = (i, j)
    
    if best_move:
        i, j = best_move
        st.session_state.board[i][j] = 2
        st.session_state.last_move = (i, j)
        return True
    return False

def reset_game():
    st.session_state.board = np.zeros((3, 3), dtype=int)
    st.session_state.game_over = False
    st.session_state.player = 1
    st.session_state.winning_line = None
    st.session_state.last_move = None
    st.session_state.winner = 0
    st.session_state.win_sound_played = False

def reset_scores():
    st.session_state.human_score = 0
    st.session_state.ai_score = 0
    st.session_state.draw_score = 0
    reset_game()

# Layout
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    # Game status with icons
    winner, win_line = check_winner(st.session_state.board)
    
    if winner != 0 and not st.session_state.win_sound_played:
        st.session_state.game_over = True
        st.session_state.winning_line = win_line
        st.session_state.winner = winner
        st.session_state.win_sound_played = True
        
        # Update scores
        if winner == 1:
            st.session_state.human_score += 1
        elif winner == 2:
            st.session_state.ai_score += 1
    
    if is_board_full(st.session_state.board) and winner == 0:
        st.session_state.game_over = True
        st.session_state.winner = 0
        st.session_state.draw_score += 1
    
    # Status display with icons
    status_container = st.empty()
    
    if st.session_state.game_over:
        if st.session_state.winner == 1:
            status_html = f'''
            <div class="status-neon" style="background: linear-gradient(45deg, #00b09b, #96c93d);">
                <i class="fas fa-trophy" style="font-size: 2rem; margin-right: 15px;"></i>
                VICTORY! You defeated the AI! 
                <i class="fas fa-crown" style="font-size: 2rem; margin-left: 15px;"></i>
            </div>
            '''
        elif st.session_state.winner == 2:
            status_html = f'''
            <div class="status-neon" style="background: linear-gradient(45deg, #f12711, #f5af19);">
                <i class="fas fa-robot" style="font-size: 2rem; margin-right: 15px;"></i>
                AI dominates! Better luck next time! 
                <i class="fas fa-skull" style="font-size: 2rem; margin-left: 15px;"></i>
            </div>
            '''
        else:
            status_html = f'''
            <div class="status-neon" style="background: linear-gradient(45deg, #8e2de2, #4a00e0);">
                <i class="fas fa-handshake" style="font-size: 2rem; margin-right: 15px;"></i>
                It's a draw! Well played! 
                <i class="fas fa-star" style="font-size: 2rem; margin-left: 15px;"></i>
            </div>
            '''
        status_container.markdown(status_html, unsafe_allow_html=True)
    elif st.session_state.player == 2:
        status_container.markdown(f'''
        <div class="status-neon" style="background: linear-gradient(45deg, #4facfe, #00f2fe);">
            <i class="fas fa-microchip" style="font-size: 2rem; margin-right: 15px;"></i>
            AI is thinking... 
            <i class="fas fa-cogs" style="font-size: 2rem; margin-left: 15px;"></i>
        </div>
        ''', unsafe_allow_html=True)
    else:
        status_container.markdown(f'''
        <div class="status-neon" style="background: linear-gradient(45deg, #667eea, #764ba2);">
            <i class="fas fa-hand-pointer" style="font-size: 2rem; margin-right: 15px;"></i>
            Your Turn! Click on any empty square 
            <i class="fas fa-times-circle" style="font-size: 2rem; margin-left: 15px; color: #ff4757;"></i>
        </div>
        ''', unsafe_allow_html=True)
    
    # Game board
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    
    # Create grid with icons
    cols = st.columns(3)
    
    for i in range(3):
        with cols[i]:
            for j in range(3):
                cell_value = st.session_state.board[i][j]
                
                # Check if this cell is part of winning line
                is_winning_cell = False
                if st.session_state.winning_line:
                    for pos in st.session_state.winning_line:
                        if pos[0] == i and pos[1] == j:
                            is_winning_cell = True
                            break
                
                if cell_value == 1:  # X
                    winning_class = "winning-cell" if is_winning_cell else ""
                    st.markdown(f'''
                    <div class="{winning_class}" style="
                        background: linear-gradient(45deg, #ff4757, #ff6b81);
                        border-radius: 15px;
                        padding: 1.5rem;
                        text-align: center;
                        margin: 5px;
                        box-shadow: 0 4px 15px rgba(255,71,87,0.3);
                    ">
                        <i class="fas fa-times x-icon"></i>
                    </div>
                    ''', unsafe_allow_html=True)
                    
                elif cell_value == 2:  # O
                    winning_class = "winning-cell" if is_winning_cell else ""
                    st.markdown(f'''
                    <div class="{winning_class}" style="
                        background: linear-gradient(45deg, #1e90ff, #70a1ff);
                        border-radius: 15px;
                        padding: 1.5rem;
                        text-align: center;
                        margin: 5px;
                        box-shadow: 0 4px 15px rgba(30,144,255,0.3);
                    ">
                        <i class="far fa-circle o-icon"></i>
                    </div>
                    ''', unsafe_allow_html=True)
                    
                else:  # Empty
                    if not st.session_state.game_over and st.session_state.player == 1:
                        button_key = f"cell_{i}_{j}_{random.randint(0, 1000)}"
                        if st.button(" ", key=button_key, help="Click to place X"):
                            if st.session_state.board[i][j] == 0 and not st.session_state.game_over:
                                # Place X
                                st.session_state.board[i][j] = 1
                                st.session_state.last_move = (i, j)
                                
                                # Check win/draw
                                winner, win_line = check_winner(st.session_state.board)
                                if winner != 0:
                                    st.session_state.game_over = True
                                    st.session_state.winning_line = win_line
                                    st.session_state.winner = winner
                                elif is_board_full(st.session_state.board):
                                    st.session_state.game_over = True
                                else:
                                    st.session_state.player = 2
                                    st.session_state.ai_thinking = True
                                
                                st.rerun()
                    else:
                        st.markdown(f'''
                        <div class="empty-cell" style="margin: 5px;">
                            <i class="fas fa-plus" style="color: rgba(255,255,255,0.2); font-size: 2rem;"></i>
                        </div>
                        ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # AI Move
    if st.session_state.player == 2 and not st.session_state.game_over:
        with st.spinner('🤖 AI is calculating optimal move...'):
            time.sleep(0.5)  # Small delay for UX
            if ai_move():
                # Check win/draw after AI move
                winner, win_line = check_winner(st.session_state.board)
                if winner != 0:
                    st.session_state.game_over = True
                    st.session_state.winning_line = win_line
                    st.session_state.winner = winner
                elif is_board_full(st.session_state.board):
                    st.session_state.game_over = True
                else:
                    st.session_state.player = 1
                
                st.session_state.ai_thinking = False
                st.rerun()
    
    # Control buttons with icons
    col_btn1, col_btn2, col_btn3, col_btn4 = st.columns([1, 1, 1, 1])
    
    with col_btn2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔄 New Game", key="new_game", use_container_width=True):
            reset_game()
            st.rerun()
    
    with col_btn3:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔄 Reset Scores", key="reset_scores", use_container_width=True):
            reset_scores()
            st.rerun()
    
    # Scoreboard with icons
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
        border-radius: 20px;
        padding: 1.5rem;
        margin-top: 1rem;
        backdrop-filter: blur(5px);
    ">
        <h3 style="text-align: center; color: white; margin-bottom: 1.5rem;">
            <i class="fas fa-chart-line"></i> SCOREBOARD <i class="fas fa-chart-line"></i>
        </h3>
    """, unsafe_allow_html=True)
    
    stats_col1, stats_col2, stats_col3 = st.columns(3)
    
    with stats_col1:
        st.markdown(f'''
        <div class="stat-card">
            <i class="fas fa-user"></i>
            <h2 style="color: #ff4757;">{st.session_state.human_score}</h2>
            <p style="color: white; font-size: 1.1rem;">HUMAN</p>
            <i class="fas fa-times" style="color: #ff4757; font-size: 1.5rem;"></i>
        </div>
        ''', unsafe_allow_html=True)
    
    with stats_col2:
        st.markdown(f'''
        <div class="stat-card">
            <i class="fas fa-robot"></i>
            <h2 style="color: #1e90ff;">{st.session_state.ai_score}</h2>
            <p style="color: white; font-size: 1.1rem;">AI</p>
            <i class="far fa-circle" style="color: #1e90ff; font-size: 1.5rem;"></i>
        </div>
        ''', unsafe_allow_html=True)
    
    with stats_col3:
        st.markdown(f'''
        <div class="stat-card">
            <i class="fas fa-handshake"></i>
            <h2 style="color: #a8e6cf;">{st.session_state.draw_score}</h2>
            <p style="color: white; font-size: 1.1rem;">DRAWS</p>
            <i class="fas fa-star" style="color: #a8e6cf; font-size: 1.5rem;"></i>
        </div>
        ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer with icons
st.markdown("""
<div style="
    position: fixed;
    bottom: 0;
    left: 0;
    width: 100%;
    text-align: center;
    padding: 1rem;
    background: rgba(0,0,0,0.5);
    backdrop-filter: blur(10px);
    color: white;
    font-size: 0.9rem;
    border-top: 1px solid rgba(255,255,255,0.1);
">
    <i class="fas fa-code"></i> Made with <i class="fas fa-heart" style="color: #ff4757;"></i> using Streamlit 
    | <i class="fas fa-crown"></i> Ultimate Tic-Tac-Toe with AI 
    | <i class="fas fa-brain"></i> Minimax Algorithm
    | <i class="fas fa-icons"></i> Icons by Font Awesome
</div>
""", unsafe_allow_html=True)

# Additional JavaScript for animations
animation_js = """
<script>
    // Add floating animation to icons
    document.querySelectorAll('.fa-robot, .fa-crown, .fa-microchip').forEach((el, i) => {
        el.style.animation = `float ${3 + i}s infinite`;
    });
    
    // Click animation
    document.querySelectorAll('button').forEach(button => {
        button.addEventListener('click', function() {
            this.style.transform = 'scale(0.95)';
            setTimeout(() => {
                this.style.transform = 'scale(1)';
            }, 100);
        });
    });
    
    // Add winning animation
    const winningCells = document.querySelectorAll('.winning-cell');
    winningCells.forEach(cell => {
        cell.style.animation = 'winGlow 1.5s infinite, pulse 1s infinite';
    });
</script>
"""
html(animation_js)