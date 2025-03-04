
import re
import pandas as pd
from pathlib import Path
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ErrorLogAnalyzer:
    def __init__(self, log_file_path):
        self.log_file_path = Path(log_file_path)
        self.market_name = self.log_file_path.stem.split('-error')[0]
        self.errors_df = pd.DataFrame(columns=[
            'market_name', 'timestamp', 'error_level', 'component_type',
            'component_name', 'error_message', 'file_path', 'line_number',
            'suggested_resolution', 'priority'
        ])

    def parse_log_entry(self, line):
        """Parse a single log entry and extract relevant information."""
        try:
            # Regular expressions for parsing different parts of the log entry
            timestamp_pattern = r'\[(.*?)\]'
            error_type_pattern = r'\[(.*?):error\]'
            pid_pattern = r'\[pid (\d+)'
            file_path_pattern = r'/wp-content/(?:plugins|themes)/([^/]+)/'
            line_number_pattern = r'on line (\d+)'
            
            # Extract timestamp
            timestamp_match = re.search(timestamp_pattern, line)
            timestamp = datetime.strptime(timestamp_match.group(1), '%a %b %d %H:%M:%S.%f %Y') if timestamp_match else None

            # Extract error type
            error_type_match = re.search(error_type_pattern, line)
            error_type = error_type_match.group(1) if error_type_match else "Unknown"

            # Extract file path and component information
            file_path_match = re.search(file_path_pattern, line)
            if file_path_match:
                component_name = file_path_match.group(1)
                component_type = 'plugin' if '/plugins/' in line else 'theme'
            else:
                component_name = 'WordPress Core'
                component_type = 'core'

            # Extract line number
            line_number_match = re.search(line_number_pattern, line)
            line_number = line_number_match.group(1) if line_number_match else None

            # Determine priority
            priority = self.determine_priority(error_type, line)

            return {
                'market_name': self.market_name,
                'timestamp': timestamp,
                'error_level': error_type,
                'component_type': component_type,
                'component_name': component_name,
                'error_message': line.split('PHP message: ')[-1].strip() if 'PHP message:' in line else line,
                'file_path': file_path_match.group(0) if file_path_match else None,
                'line_number': line_number,
                'suggested_resolution': self.suggest_resolution(error_type, component_name),
                'priority': priority
            }
        except Exception as e:
            logger.error(f"Error parsing log entry: {e}")
            return None

    def determine_priority(self, error_type, message):
        """Determine the priority of the error."""
        if 'Fatal' in error_type or 'client denied' in message:
            return 'High'
        elif 'Warning' in error_type:
            return 'Medium'
        else:
            return 'Low'

    def suggest_resolution(self, error_type, component):
        """Suggest resolution based on error type and component."""
        suggestions = {
            'client denied': 'Check server configuration and access permissions',
            'Undefined variable': f'Review variable initialization in {component}',
            'Undefined array key': f'Verify array keys and data structure in {component}',
            'Fatal error': f'Critical review needed for {component}'
        }

        for error_pattern, resolution in suggestions.items():
            if error_pattern in error_type:
                return resolution
        return 'Investigate and review code'

    def analyze_log_file(self):
        """Read and analyze the log file."""
        try:
            with open(self.log_file_path, 'r') as file:
                entries = []
                for line in file:
                    if ':error]' in line:  # Only process error lines
                        parsed_entry = self.parse_log_entry(line)
                        if parsed_entry:
                            entries.append(parsed_entry)
                
                self.errors_df = pd.DataFrame(entries)
                return True
        except Exception as e:
            logger.error(f"Error analyzing log file: {e}")
            return False

    def generate_report(self):
        """Generate CSV report with analyzed errors."""
        try:
            output_path = Path(f'analysis_{self.market_name}_{datetime.now().strftime("%Y%m%d")}.csv')
            self.errors_df.to_csv(output_path, index=False)
            logger.info(f"Report generated: {output_path}")

            # Generate summary statistics
            summary = {
                'total_errors': len(self.errors_df),
                'by_priority': self.errors_df['priority'].value_counts().to_dict(),
                'by_component': self.errors_df['component_name'].value_counts().to_dict()
            }
            
            logger.info("Analysis Summary:")
            logger.info(f"Total Errors: {summary['total_errors']}")
            logger.info(f"Errors by Priority: {summary['by_priority']}")
            logger.info(f"Errors by Component: {summary['by_component']}")
            
            return summary
        except Exception as e:
            logger.error(f"Error generating report: {e}")
            return None

def main():
    # Initialize the analyzer with markets log file
    log_file = Path('')
    analyzer = ErrorLogAnalyzer(log_file)
    
    # Analyze the log file
    if analyzer.analyze_log_file():
        # Generate and display report
        summary = analyzer.generate_report()
        if summary:
            logger.info("Analysis completed successfully")
    else:
        logger.error("Analysis failed")

if __name__ == "__main__":
    main()
