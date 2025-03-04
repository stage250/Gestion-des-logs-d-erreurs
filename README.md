# Error Log Analysis Tool

A Python tool to analyze and classify WordPress error logs from multiple markets.

## Objective

Parse error log files to:
- Identify different types of errors (Notice, Warning, Fatal)  
- Classify them by plugin/theme
- Generate CSV reports per market
- Provide insights for resolution

## Methodology

### 1. Log File Processing

#### Input Structure
- One log file per market
- Standard Apache/PHP error log format
- Contains timestamps, error types, file paths, and error messages

#### Error Classification
Three main categories:
- Notice: PHP Notice messages
- Warning: PHP Warning messages
- Fatal: Fatal errors, access denied, critical failures

### 2. Data Extraction

For each error entry, extract:
- Timestamp
- Error Type
- Source (Plugin/Theme path)
- Error Message
- Context (referer URL if available)
- Process ID (PID)

### 3. Plugin/Theme Identification

Identify source by path patterns:
- `/wp-content/plugins/{plugin-name}/` -> Plugin errors
- `/wp-content/themes/{theme-name}/` -> Theme errors
- Other paths -> Core WordPress or server errors

### 4. CSV Structure

Output columns:
- Market Name
- Timestamp
- Error Level
- Component Type (Plugin/Theme/Core)
- Component Name
- Error Message
- File Path
- Line Number
- Suggested Resolution
- Priority (High/Medium/Low)

### 5. Priority Classification

Define priority based on:
- Error Type (Fatal = High, Warning = Medium, Notice = Low)
- Frequency of occurrence
- Impact on functionality
- Security implications

### 6. Implementation Steps

1. File Reading
   - Read each .log file
   - Parse log entries using regex patterns
   
2. Error Processing
   - Extract relevant information
   - Classify error types
   - Identify affected components
   
3. Data Organization
   - Group by market
   - Sort by priority
   - Aggregate similar errors
   
4. Report Generation
   - Create CSV files
   - Generate summary statistics
   - Include resolution hints

## Required Python Libraries

- pandas: Data manipulation and CSV handling
- re: Regular expression operations
- pathlib: File path handling
- datetime: Timestamp processing

## Expected Output

One CSV file per market containing:
- Classified errors
- Component identification
- Priority levels
- Suggested fixes

## Notes

- Handle log rotation and date ranges
- Consider error frequency patterns
- Group similar errors for efficient analysis
- Track recurring issues across markets
