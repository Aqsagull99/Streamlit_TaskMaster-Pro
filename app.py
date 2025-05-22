import streamlit as st
from datetime import datetime, date
import random
import time
from enum import Enum
import pandas as pd
import plotly.express as px

# ======================
# OOP IMPLEMENTATION
# ======================

class TaskPriority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    URGENT = 4

class Task:
    def __init__(self, title, description, due_date, priority=TaskPriority.MEDIUM, completed=False):
        self.title = title
        self.description = description
        # Ensure due_date is always a date object
        if isinstance(due_date, datetime):
            self.due_date = due_date.date()
        else:
            self.due_date = due_date
        self.priority = priority
        self.completed = completed
        self.created_at = datetime.now()
        self.completed_at = None
        
    def complete_task(self):
        self.completed = True
        self.completed_at = datetime.now()
        
    def __str__(self):
        return f"{self.title} (Due: {self.due_date.strftime('%Y-%m-%d')}, Priority: {self.priority.name})"

class User:
    def __init__(self, username, email, is_premium=False, subscription_end=None):
        self.username = username
        self.email = email
        self.is_premium = is_premium
        self.subscription_end = subscription_end
        self.tasks = []
        
    def add_task(self, task):
        self.tasks.append(task)
        
    def complete_task(self, task_index):
        if 0 <= task_index < len(self.tasks):
            self.tasks[task_index].complete_task()
            
    def get_completed_tasks(self):
        return [task for task in self.tasks if task.completed]
    
    def get_pending_tasks(self):
        return [task for task in self.tasks if not task.completed]
    
    def upgrade_to_premium(self, months=1):
        self.is_premium = True
        if self.subscription_end is None or self.subscription_end < datetime.now():
            self.subscription_end = datetime.now()
        self.subscription_end = self.subscription_end.replace(month=self.subscription_end.month + months)

class TaskManager:
    def __init__(self):
        self.users = {}
        
    def register_user(self, username, email):
        if username not in self.users:
            self.users[username] = User(username, email)
            return True
        return False
    
    def login_user(self, username):
        return self.users.get(username)
    
    def get_user_stats(self, username):
        if username in self.users:
            user = self.users[username]
            return {
                'total_tasks': len(user.tasks),
                'completed_tasks': len(user.get_completed_tasks()),
                'pending_tasks': len(user.get_pending_tasks()),
                'premium_user': user.is_premium
            }
        return None

# ======================
# SIMULATED DATABASE
# ======================

class DatabaseSimulator:
    def __init__(self):
        self.task_manager = TaskManager()
        # Add some dummy users
        self.task_manager.register_user("Aqsa", "Aqsa@example.com")
        self.task_manager.register_user("Aqsa_Gull", "AqsaGull@example.com")
        
        # Add some dummy tasks
        john = self.task_manager.login_user("Aqsa")
        if john:
            john.add_task(Task("Complete project", "Finish the Streamlit assignment", datetime(2023, 6, 15), TaskPriority.HIGH))
            john.add_task(Task("Buy groceries", "Milk, eggs, bread", datetime(2023, 6, 10), TaskPriority.MEDIUM))
            john.add_task(Task("Call mom", "Wish her happy birthday", datetime(2023, 6, 12), TaskPriority.URGENT))
            john.add_task(Task("Exercise", "30 minutes cardio", datetime(2023, 6, 11), TaskPriority.LOW, True))
        
        jane = self.task_manager.login_user("Aqsa_Gull")
        if jane:
            jane.upgrade_to_premium(3)
            jane.add_task(Task("Prepare presentation", "Quarterly business review", datetime(2023, 6, 20), TaskPriority.HIGH))
            jane.add_task(Task("Book flights", "Summer vacation", datetime(2023, 7, 1), TaskPriority.MEDIUM))
            jane.add_task(Task("Renew subscription", "TaskMaster Pro", datetime(2023, 6, 30), TaskPriority.URGENT))

# ======================
# STREAMLIT UI
# ======================

def main():
    # Initialize simulated database
    db = DatabaseSimulator()
    
    # Set page config
    st.set_page_config(
        page_title="TaskMaster Pro",
        page_icon="✅",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS for professional look
    st.markdown("""
    <style>
        .main {
            background-color: #f8f9fa;
        }
        .sidebar .sidebar-content {
            background-color: #343a40;
            color: white;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            border-radius: 4px;
            padding: 0.5em 1em;
        }
        .stTextInput>div>div>input {
            border-radius: 4px;
        }
        .stDateInput>div>div>input {
            border-radius: 4px;
        }
        .stSelectbox>div>div>select {
            border-radius: 4px;
        }
        .task-card {
            padding: 1em;
            margin: 0.5em 0;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            background-color: white;
        }
        .premium-badge {
            background-color: #ffc107;
            color: black;
            padding: 0.2em 0.5em;
            border-radius: 12px;
            font-size: 0.8em;
            font-weight: bold;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Sidebar for authentication
    st.sidebar.title("TaskMaster Pro")
    st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/a/a7/React-icon.svg/1200px-React-icon.svg.png", use_container_width=True)
    
    # Authentication simulation
    if 'logged_in_user' not in st.session_state:
        st.session_state.logged_in_user = None
    
    if st.session_state.logged_in_user is None:
        st.sidebar.subheader("Login")
        username = st.sidebar.text_input("Username")
        if st.sidebar.button("Login"):
            user = db.task_manager.login_user(username)
            if user:
                st.session_state.logged_in_user = user
                st.sidebar.success(f"Welcome back, {user.username}!")
                time.sleep(1)
                st.rerun()
            else:
                st.sidebar.error("User not found")
        
        st.sidebar.subheader("Or Register")
        new_username = st.sidebar.text_input("Choose username")
        new_email = st.sidebar.text_input("Email")
       
        if st.sidebar.button("Create Account"):
            if db.task_manager.register_user(new_username, new_email):
                st.sidebar.success("Account created! Please login.")
            else:
                st.sidebar.error("Username already exists")
    else:
        user = st.session_state.logged_in_user
        st.sidebar.subheader(f"Welcome, {user.username}")
        if user.is_premium:
            st.sidebar.markdown(f'<span class="premium-badge">PREMIUM USER</span>', unsafe_allow_html=True)
            st.sidebar.write(f"Subscription valid until: {user.subscription_end.strftime('%Y-%m-%d')}")
        else:
            st.sidebar.write("Free account")
        
        stats = db.task_manager.get_user_stats(user.username)
        st.sidebar.write(f"📊 Tasks: {stats['pending_tasks']} pending, {stats['completed_tasks']} completed")
        
        if st.sidebar.button("Logout"):
            st.session_state.logged_in_user = None
            st.rerun()
    
    # Main content area
    if st.session_state.logged_in_user is None:
        st.title("Boost Your Productivity with TaskMaster Pro")
        st.subheader("The ultimate task management solution")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            ### 🚀 Key Features
            - AI-powered task prioritization
            - Cross-device synchronization
            - Team collaboration tools
            - Time tracking and analytics
            - Customizable workflows
            """)
        
        with col2:
            st.markdown("""
            ### 💎 Premium Benefits
            - Unlimited projects
            - Advanced analytics
            - Priority support
            - File attachments
            - Calendar integration
            """)
        
        with col3:
            st.markdown("""
            ### 📈 Business Solutions
            - Team management
            - Admin controls
            - Productivity reports
            - API access
            - Dedicated account manager
            """)
        
        st.markdown("---")
        st.subheader("Ready to get started?")
        st.write("Login or create an account from the sidebar to begin organizing your tasks!")
        
        # Testimonials
        st.markdown("""
        ## What Our Users Say
        """)
        testimonial_cols = st.columns(2)
        with testimonial_cols[0]:
            st.markdown("""
            > "TaskMaster Pro has transformed how I organize my work. The AI prioritization saves me hours every week!"
            >
            > **— Sarah J., Marketing Director**
            """)
        with testimonial_cols[1]:
            st.markdown("""
            > "As a freelancer, I need to stay on top of multiple projects. This app keeps me organized and productive."
            >
            > **— Michael T., Graphic Designer**
            """)
        
    else:
        user = st.session_state.logged_in_user
        st.title(f"Your Tasks, {user.username}")
        
        # Task management tabs
        tab1, tab2, tab3, tab4 = st.tabs(["📋 All Tasks", "✅ Completed", "⏳ Pending", "📊 Analytics"])
        
        with tab1:
            st.subheader("All Tasks")
            if not user.tasks:
                st.info("You don't have any tasks yet. Add one below!")
            else:
                for i, task in enumerate(user.tasks):
                    with st.expander(f"{'✔️' if task.completed else '🔘'} {task.title}"):
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.write(f"**Description:** {task.description}")
                            st.write(f"**Due Date:** {task.due_date.strftime('%Y-%m-%d')}")
                            st.write(f"**Priority:** {task.priority.name}")
                            if task.completed:
                                st.write(f"**Completed on:** {task.completed_at.strftime('%Y-%m-%d')}")
                            else:
                                if st.button("Mark Complete", key=f"complete_{i}"):
                                    user.complete_task(i)
                                    st.success("Task marked as complete!")
                                    time.sleep(1)
                                    st.rerun()
                        with col2:
                            current_date = date.today()
                            days_left = (task.due_date - current_date).days
                            
                            if not task.completed:
                                if days_left < 0:
                                    st.error(f"Overdue by {-days_left} days")
                                elif days_left == 0:
                                    st.warning("Due today")
                                elif days_left <= 3:
                                    st.warning(f"Due in {days_left} days")
                                else:
                                    st.info(f"Due in {days_left} days")
        
        with tab2:
            st.subheader("Completed Tasks")
            completed_tasks = user.get_completed_tasks()
            if not completed_tasks:
                st.info("No completed tasks yet")
            else:
                for task in completed_tasks:
                    st.markdown(f"""
                    <div class="task-card">
                        <h4>✔️ {task.title}</h4>
                        <p>Completed on: {task.completed_at.strftime('%Y-%m-%d')}</p>
                    </div>
                    """, unsafe_allow_html=True)
        
        with tab3:
            st.subheader("Pending Tasks")
            pending_tasks = user.get_pending_tasks()
            if not pending_tasks:
                st.info("No pending tasks - great job!")
            else:
                for task in pending_tasks:
                    current_date = date.today()
                    days_left = (task.due_date - current_date).days
                    status = ""
                    if days_left < 0:
                        status = f"❌ Overdue by {-days_left} days"
                    elif days_left == 0:
                        status = "⚠️ Due today"
                    elif days_left <= 3:
                        status = f"⚠️ Due in {days_left} days"
                    else:
                        status = f"⏳ Due in {days_left} days"
                    
                    st.markdown(f"""
                    <div class="task-card">
                        <h4>🔘 {task.title}</h4>
                        <p>Priority: {task.priority.name} | Due: {task.due_date.strftime('%Y-%m-%d')} | {status}</p>
                        <p>{task.description}</p>
                    </div>
                    """, unsafe_allow_html=True)
        
        with tab4:
            st.subheader("Productivity Analytics")
            if not user.tasks:
                st.info("No data to display yet. Add some tasks first!")
            else:
                # Create DataFrame for visualization
                tasks_data = []
                for task in user.tasks:
                    current_date = date.today()
                    days_left = (task.due_date - current_date).days if not task.completed else None
                    
                    tasks_data.append({
                        'Title': task.title,
                        'Priority': task.priority.name,
                        'Due Date': task.due_date,
                        'Completed': task.completed,
                        'Days Left': days_left,
                        'Completion Time': (task.completed_at - task.created_at).days if task.completed else None
                    })
                
                df = pd.DataFrame(tasks_data)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Completion rate pie chart
                    if len(user.tasks) > 0:
                        completed_count = len(user.get_completed_tasks())
                        pending_count = len(user.get_pending_tasks())
                        fig = px.pie(
                            names=['Completed', 'Pending'],
                            values=[completed_count, pending_count],
                            title='Task Completion Rate',
                            color=['Completed', 'Pending'],
                            color_discrete_map={'Completed':'#2ecc71','Pending':'#e74c3c'}
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.info("Not enough data for completion rate chart")
                
                with col2:
                    # Priority distribution
                    if len(user.tasks) > 0:
                        priority_counts = df['Priority'].value_counts().reset_index()
                        priority_counts.columns = ['Priority', 'Count']
                        fig = px.bar(
                            priority_counts,
                            x='Priority',
                            y='Count',
                            title='Task Priority Distribution',
                            color='Priority'
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.info("Not enough data for priority distribution chart")
                
                # Premium features section
                if not user.is_premium:
                    st.markdown("---")
                    st.subheader("🔓 Unlock Advanced Analytics")
                    st.write("Upgrade to Premium to access:")
                    st.write("- Historical performance trends")
                    st.write("- Time spent analysis")
                    st.write("- Custom report generation")
                    st.write("- Team productivity metrics")
                    
                    if st.button("Upgrade to Premium", key="upgrade_analytics"):
                        st.session_state.show_upgrade = True
                        st.rerun()
        
        # Add new task form
        st.markdown("---")
        with st.expander("➕ Add New Task"):
            with st.form("add_task_form"):
                title = st.text_input("Task Title", max_chars=100)
                description = st.text_area("Description")
                due_date = st.date_input("Due Date", min_value=date.today())
                priority = st.selectbox(
                    "Priority",
                    options=[p.name for p in TaskPriority],
                    index=1
                )
                
                if st.form_submit_button("Add Task"):
                    if title:
                        priority_enum = TaskPriority[priority]
                        new_task = Task(
                            title=title,
                            description=description,
                            due_date=due_date,
                            priority=priority_enum
                        )
                        user.add_task(new_task)
                        st.success("Task added successfully!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("Please enter a task title")
        
        # Premium upgrade section
        if not user.is_premium:
            st.markdown("---")
            st.subheader("🚀 Upgrade to Premium")
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                ### 💎 Premium Features
                - Unlimited projects
                - Advanced analytics
                - File attachments (up to 100MB)
                - Calendar integration
                - Priority support
                - AI task suggestions
                """)
            
            with col2:
                st.markdown("""
                ### Pricing Plans
                """)
                
                plan_cols = st.columns(2)
                
                with plan_cols[0]:
                    st.markdown("""
                    **Monthly**  
                    $5/month  
                    Cancel anytime
                    """)
                    if st.button("Choose Monthly", key="monthly_plan"):
                        st.session_state.show_upgrade = True
                
                with plan_cols[1]:
                    st.markdown("""
                    **Annual (Save 20%)**  
                    $48/year ($4/month)  
                    Billed annually
                    """)
                    if st.button("Choose Annual", key="annual_plan"):
                        st.session_state.show_upgrade = True
            
            st.markdown("""
            *7-day money-back guarantee. All plans include all premium features.*
            """)
        
        # Payment simulation
        if st.session_state.get('show_upgrade', False):
            with st.form("payment_form"):
                st.subheader("Upgrade to Premium")
                st.write("Please enter your payment details")
                
                name_on_card = st.text_input("Name on Card")
                card_number = st.text_input("Card Number", placeholder="1234 5678 9012 3456")
                
                col1, col2 = st.columns(2)
                with col1:
                    expiry_date = st.text_input("Expiry Date", placeholder="MM/YY")
                with col2:
                    cvv = st.text_input("CVV", placeholder="123")
                
                promo_code = st.text_input("Promo Code (optional)")
                
                if st.form_submit_button("Subscribe Now"):
                    if name_on_card and card_number and expiry_date and cvv:
                        # Simulate payment processing
                        with st.spinner("Processing payment..."):
                            time.sleep(2)
                            
                            # Randomly simulate payment success/failure
                            if random.random() > 0.2:  # 80% success rate
                                user.upgrade_to_premium(12 if st.session_state.get('annual_plan', False) else 1)
                                st.success("Payment successful! You are now a Premium member.")
                                st.balloons()
                                st.session_state.show_upgrade = False
                                time.sleep(2)
                                st.rerun()
                            else:
                                st.error("Payment failed. Please check your card details and try again.")
                    else:
                        st.error("Please fill in all payment details")

if __name__ == "__main__":
    main()




