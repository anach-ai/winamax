"""
Winamax Socket.IO Traffic Analyzer
Author: Anass EL
Description: Captures and analyzes Socket.IO traffic from Winamax sports betting page using Selenium stealth
"""
import time
import json
import logging
import sys
from typing import List, Dict, Any
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException

from selenium_stealth import stealth
from selenium.webdriver.common.action_chains import ActionChains

try:
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.chrome.service import Service as ChromeService
    USE_WEBDRIVER_MANAGER = True
except ImportError:
    USE_WEBDRIVER_MANAGER = False

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('winamax_socketio.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class SocketIOCapture:
    """Capture Socket.IO messages using Selenium stealth"""
    
    def __init__(self):
        self.url = "https://www.winamax.fr/paris-sportifs/sports/1"
        self.driver = None
        self.messages: List[Dict[str, Any]] = []
        self.setup_driver()
    
    def setup_driver(self):
        """Setup Chrome driver with stealth and logging"""
        logger.info("Setting up Chrome driver with stealth...")
        
        options = Options()
        
        # Anti-detection options
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-gpu")
        
        # User agent
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
        options.add_argument(f"--user-agent={user_agent}")
        
        # Enable Chrome DevTools Protocol for network logging
        options.add_argument("--enable-logging")
        options.add_argument("--log-level=3")
        options.set_capability('goog:loggingPrefs', {'performance': 'ALL', 'browser': 'ALL'})
        
        # Start driver with automatic driver management if available
        if USE_WEBDRIVER_MANAGER:
            service = ChromeService(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
        else:
            self.driver = webdriver.Chrome(options=options)
        
        # Apply stealth
        stealth(
            self.driver,
            languages=["en-US", "en", "ar", "fr"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
        )
        
        logger.info("Chrome driver initialized with stealth")
    
    def inject_socketio_capture(self):
        """Inject JavaScript to capture Socket.IO messages"""
        logger.info("Injecting Socket.IO capture script...")
        
        capture_script = """
        // Store original Socket.IO methods
        window.capturedMessages = [];
        
        // Function to capture messages
        window.captureSocketIOMessage = function(event, data) {
            window.capturedMessages.push({
                timestamp: new Date().toISOString(),
                event: event,
                data: data
            });
            console.log('[SOCKET.IO CAPTURE]', event, data);
        };
        
        // Override io if it exists
        if (typeof io !== 'undefined') {
            console.log('[SOCKET.IO CAPTURE] Socket.IO found, setting up interception...');
            
            const originalIo = io;
            window.io = function(url, options) {
                const socket = originalIo(url, options);
                
                // Capture connect
                socket.on('connect', function() {
                    window.captureSocketIOMessage('connect', {});
                });
                
                // Capture disconnect
                socket.on('disconnect', function(reason) {
                    window.captureSocketIOMessage('disconnect', {reason: reason});
                });
                
                // Capture all events
                const originalOn = socket.on;
                socket.on = function(event, callback) {
                    console.log('[SOCKET.IO CAPTURE] Registered event:', event);
                    
                    // Wrap the callback
                    const wrappedCallback = function(...args) {
                        window.captureSocketIOMessage(event, args);
                        return callback.apply(this, args);
                    };
                    
                    return originalOn.call(this, event, wrappedCallback);
                };
                
                // Capture emitted messages
                const originalEmit = socket.emit;
                socket.emit = function(event, ...args) {
                    window.captureSocketIOMessage('emit_' + event, args);
                    return originalEmit.apply(this, [event, ...args]);
                };
                
                return socket;
            };
        }
        
        // Also try to capture WebSocket directly
        if (typeof WebSocket !== 'undefined') {
            const OriginalWebSocket = WebSocket;
            window.WebSocket = function(url, protocols) {
                const ws = new OriginalWebSocket(url, protocols);
                
                ws.addEventListener('message', function(event) {
                    try {
                        const data = JSON.parse(event.data);
                        window.captureSocketIOMessage('websocket_message', data);
                    } catch (e) {
                        window.captureSocketIOMessage('websocket_message', {raw: event.data});
                    }
                }, true);
                
                ws.addEventListener('open', function() {
                    window.captureSocketIOMessage('websocket_open', {url: url});
                }, true);
                
                ws.addEventListener('close', function(event) {
                    window.captureSocketIOMessage('websocket_close', {
                        code: event.code,
                        reason: event.reason
                    });
                }, true);
                
                return ws;
            };
        }
        
        console.log('[SOCKET.IO CAPTURE] Interception script loaded');
        """
        
        self.driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {'source': capture_script})
        logger.info("Socket.IO capture script injected")
    
    def load_page(self):
        """Load the Winamax page"""
        logger.info(f"Loading page: {self.url}")
        self.driver.get(self.url)
        
        # Wait for page to load
        time.sleep(3)
        
        # Try to inject capture script
        try:
            self.driver.execute_script("""
                console.log('[SOCKET.IO CAPTURE] Page loaded, checking for Socket.IO...');
            """)
        except Exception as e:
            logger.warning(f"Could not inject initial script: {e}")
    
    def analyze_network_logs(self):
        """Analyze Chrome DevTools Protocol logs for Socket.IO traffic"""
        logger.info("Analyzing network logs...")
        
        try:
            logs = self.driver.get_log('performance')
            for log in logs:
                message = json.loads(log['message'])
                method = message.get('message', {}).get('method', '')
                params = message.get('message', {}).get('params', {})
                
                # Look for WebSocket related messages
                if 'Network.webSocket' in method or 'Network.webSocketFrame' in method:
                    self.messages.append({
                        'timestamp': log['timestamp'],
                        'method': method,
                        'params': params
                    })
                    logger.info(f"Found WebSocket message: {method}")
        
        except Exception as e:
            logger.error(f"Error analyzing network logs: {e}")
    
    def collect_captured_messages(self):
        """Collect messages captured by injected JavaScript"""
        logger.info("Collecting captured messages...")
        
        try:
            messages = self.driver.execute_script("return window.capturedMessages || [];")
            if messages:
                self.messages.extend(messages)
                logger.info(f"Collected {len(messages)} captured messages")
                
                # Clear captured messages
                self.driver.execute_script("window.capturedMessages = [];")
        except Exception as e:
            logger.warning(f"Could not collect captured messages: {e}")
    
    def wait_for_socketio_activity(self, duration: int = 30):
        """Wait and monitor for Socket.IO activity with auto-scrolling"""
        logger.info(f"Monitoring Socket.IO activity for {duration} seconds...")
        
        start_time = time.time()
        check_interval = 2  # Check every 2 seconds
        scroll_interval = 5  # Scroll every 5 seconds
        last_scroll_time = 0
        
        while time.time() - start_time < duration:
            # Collect captured messages
            self.collect_captured_messages()
            
            # Auto-scroll to load more matches
            current_time = time.time()
            if current_time - last_scroll_time >= scroll_interval:
                try:
                    # Scroll down to trigger lazy loading
                    self.driver.execute_script("window.scrollBy(0, 1000);")
                    last_scroll_time = current_time
                except:
                    pass
            
            # Check for Socket.IO in console logs
            try:
                logs = self.driver.get_log('browser')
                for log in logs:
                    if '[SOCKET.IO' in log['message']:
                        logger.info(f"Console: {log['message']}")
            except:
                pass
            
            time.sleep(check_interval)
        
        logger.info("Monitoring complete")
    
    def save_results(self, filename: str = "winamax_socketio_analysis.json"):
        """Save analysis results to JSON file"""
        logger.info(f"Saving results to {filename}...")
        
        output = {
            'url': self.url,
            'timestamp': datetime.now().isoformat(),
            'message_count': len(self.messages),
            'messages': self.messages
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Results saved to {filename}")
        
        # Also print summary
        print("\n" + "="*80)
        print("WINAMAX SOCKET.IO ANALYSIS SUMMARY")
        print("="*80)
        print(f"Total messages captured: {len(self.messages)}")
        print(f"Results saved to: {filename}")
        print("="*80)
        
        if self.messages:
            print("\nMessage types:")
            event_types = {}
            for msg in self.messages:
                event = msg.get('event', msg.get('method', 'unknown'))
                event_types[event] = event_types.get(event, 0) + 1
            
            for event, count in sorted(event_types.items(), key=lambda x: x[1], reverse=True):
                print(f"  {event}: {count}")
        else:
            print("\nNo messages captured. Socket.IO might not be used or detection failed.")
    
    def run(self, duration: int = 30):
        """Run the complete analysis"""
        try:
            logger.info("Starting Winamax Socket.IO analysis...")
            
            # Inject capture script first
            self.inject_socketio_capture()
            
            # Load page
            self.load_page()
            
            # Monitor for activity
            self.wait_for_socketio_activity(duration)
            
            # Analyze network logs
            self.analyze_network_logs()
            
            # Save results
            self.save_results()
            
        except Exception as e:
            logger.error(f"Error during analysis: {e}", exc_info=True)
        finally:
            if self.driver:
                logger.info("Closing browser...")
                time.sleep(2)  # Give time for final messages
                self.driver.quit()
    
    def cleanup(self):
        """Clean up resources"""
        if self.driver:
            self.driver.quit()

def main():
    """Main entry point"""
    print("\nWinamax Socket.IO Traffic Analyzer")
    print("="*50)
    print("This script will:")
    print("1. Load the Winamax sports betting page")
    print("2. Capture Socket.IO and WebSocket traffic")
    print("3. Analyze the captured messages")
    print("4. Save results to JSON file")
    print("="*50)
    
    # Get duration from command line argument or default
    duration = 30
    if len(sys.argv) > 1:
        try:
            duration = int(sys.argv[1])
        except ValueError:
            print(f"Invalid duration argument: {sys.argv[1]}, using default 30 seconds")
    else:
        print("\nUsing default duration: 30 seconds")
        print("You can specify custom duration: python analyze_winamax_socketio.py <seconds>")
    
    # Run analysis
    analyzer = SocketIOCapture()
    try:
        analyzer.run(duration=duration)
    except KeyboardInterrupt:
        print("\n\nAnalysis interrupted by user")
        analyzer.cleanup()
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        analyzer.cleanup()

if __name__ == "__main__":
    main()

