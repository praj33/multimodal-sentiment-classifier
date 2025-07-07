#!/usr/bin/env python3
"""
🎯 Uniguru Sentiment Agent CLI Interface
Command-line interface for easy testing and integration

🚀 Features:
- Interactive CLI mode
- Batch processing
- JSON file input/output
- Real-time analysis
- Persona switching
- Export capabilities

🎓 Designed for Educational Excellence by Raj
"""

import asyncio
import argparse
import json
import sys
import os
from typing import Dict, Any, List
import time
from datetime import datetime

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sentiment_agent_adapter import predict

class UniguruCLI:
    """Command-line interface for Uniguru Sentiment Agent"""
    
    def __init__(self):
        self.session_history = []
        self.current_persona = "youth"
        
    def print_banner(self):
        """Print CLI banner"""
        print("🎓" + "=" * 58 + "🎓")
        print("   UNIGURU SENTIMENT AGENT - CLI INTERFACE")
        print("   Production-grade sentiment analysis for education")
        print("   Designed by Raj for Advanced Implementation")
        print("🎓" + "=" * 58 + "🎓")
        print()
    
    def print_help(self):
        """Print available commands"""
        print("📋 AVAILABLE COMMANDS:")
        print("  analyze <text>          - Analyze text sentiment")
        print("  image <url>             - Analyze image from URL")
        print("  multimodal <text> <url> - Analyze text + image")
        print("  persona <youth|kids|spiritual> - Switch persona")
        print("  batch <file.json>       - Process batch file")
        print("  export <file.json>      - Export session history")
        print("  history                 - Show session history")
        print("  clear                   - Clear session history")
        print("  help                    - Show this help")
        print("  quit                    - Exit CLI")
        print()
    
    def format_result(self, result: Dict[str, Any]) -> str:
        """Format analysis result for display"""
        if "error" in result:
            return f"❌ Error: {result['error']}\n   Details: {result.get('details', 'N/A')}"
        
        output = []
        output.append(f"🎯 SENTIMENT: {result['sentiment'].upper()}")
        output.append(f"🎭 TONE: {result['tone']}")
        output.append(f"📊 CONFIDENCE: {result['confidence']:.3f}")
        output.append(f"🗣️  TTS EMOTION: {result['tts_emotion']}")
        output.append(f"👤 PERSONA: {result['persona']}")
        
        if "language" in result:
            output.append(f"🌍 LANGUAGE: {result['language']}")
        
        output.append(f"⏱️  PROCESSING: {result['processing_time_ms']:.2f}ms")
        
        # Input summary
        summary = result.get("input_summary", {})
        modalities = []
        if summary.get("has_text"): modalities.append("text")
        if summary.get("has_image"): modalities.append("image")
        if summary.get("has_audio"): modalities.append("audio")
        
        if modalities:
            output.append(f"📝 MODALITIES: {', '.join(modalities)}")
        
        return "\n".join(output)
    
    async def analyze_text(self, text: str) -> Dict[str, Any]:
        """Analyze text sentiment"""
        return await predict({
            "text": text,
            "persona": self.current_persona
        })
    
    async def analyze_image(self, image_url: str) -> Dict[str, Any]:
        """Analyze image sentiment"""
        return await predict({
            "image_url": image_url,
            "persona": self.current_persona
        })
    
    async def analyze_multimodal(self, text: str, image_url: str) -> Dict[str, Any]:
        """Analyze multimodal input"""
        return await predict({
            "text": text,
            "image_url": image_url,
            "persona": self.current_persona
        })
    
    async def process_batch_file(self, filename: str):
        """Process batch JSON file"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                batch_data = json.load(f)
            
            if not isinstance(batch_data, list):
                batch_data = [batch_data]
            
            print(f"📦 Processing {len(batch_data)} items from {filename}")
            print("-" * 50)
            
            results = []
            for i, item in enumerate(batch_data, 1):
                print(f"\n🔄 Processing item {i}/{len(batch_data)}")
                
                # Add current persona if not specified
                if "persona" not in item:
                    item["persona"] = self.current_persona
                
                result = await predict(item)
                results.append({
                    "input": item,
                    "output": result,
                    "timestamp": datetime.now().isoformat()
                })
                
                print(self.format_result(result))
                
                # Add to session history
                self.session_history.append({
                    "command": f"batch_item_{i}",
                    "input": item,
                    "result": result,
                    "timestamp": datetime.now().isoformat()
                })
            
            # Save results
            output_filename = f"batch_results_{int(time.time())}.json"
            with open(output_filename, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            
            print(f"\n✅ Batch processing completed!")
            print(f"📄 Results saved to: {output_filename}")
            
        except FileNotFoundError:
            print(f"❌ File not found: {filename}")
        except json.JSONDecodeError as e:
            print(f"❌ Invalid JSON in file: {e}")
        except Exception as e:
            print(f"❌ Batch processing error: {e}")
    
    def export_history(self, filename: str):
        """Export session history to JSON file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.session_history, f, indent=2, ensure_ascii=False)
            print(f"✅ Session history exported to: {filename}")
        except Exception as e:
            print(f"❌ Export error: {e}")
    
    def show_history(self):
        """Show session history"""
        if not self.session_history:
            print("📝 No session history available")
            return
        
        print(f"📚 SESSION HISTORY ({len(self.session_history)} items)")
        print("-" * 50)
        
        for i, entry in enumerate(self.session_history[-10:], 1):  # Show last 10
            print(f"\n{i}. {entry['command']} - {entry['timestamp']}")
            if "result" in entry and "sentiment" in entry["result"]:
                result = entry["result"]
                print(f"   🎯 {result['sentiment']} ({result['confidence']:.3f}) - {result['tone']}")
    
    async def interactive_mode(self):
        """Run interactive CLI mode"""
        self.print_banner()
        print(f"🎭 Current persona: {self.current_persona}")
        print("💡 Type 'help' for available commands")
        print()
        
        while True:
            try:
                # Get user input
                user_input = input("🎓 uniguru> ").strip()
                
                if not user_input:
                    continue
                
                # Parse command
                parts = user_input.split(maxsplit=1)
                command = parts[0].lower()
                args = parts[1] if len(parts) > 1 else ""
                
                start_time = time.time()
                
                # Process commands
                if command == "quit" or command == "exit":
                    print("👋 Goodbye! Thanks for using Uniguru Sentiment Agent!")
                    break
                
                elif command == "help":
                    self.print_help()
                
                elif command == "clear":
                    self.session_history.clear()
                    print("🧹 Session history cleared")
                
                elif command == "history":
                    self.show_history()
                
                elif command == "persona":
                    if args in ["youth", "kids", "spiritual"]:
                        self.current_persona = args
                        print(f"🎭 Persona switched to: {self.current_persona}")
                    else:
                        print("❌ Invalid persona. Use: youth, kids, or spiritual")
                
                elif command == "analyze":
                    if not args:
                        print("❌ Please provide text to analyze")
                        continue
                    
                    print("🔄 Analyzing text...")
                    result = await self.analyze_text(args)
                    print(self.format_result(result))
                    
                    # Add to history
                    self.session_history.append({
                        "command": "analyze",
                        "input": args,
                        "result": result,
                        "timestamp": datetime.now().isoformat()
                    })
                
                elif command == "image":
                    if not args:
                        print("❌ Please provide image URL")
                        continue
                    
                    print("🔄 Analyzing image...")
                    result = await self.analyze_image(args)
                    print(self.format_result(result))
                    
                    # Add to history
                    self.session_history.append({
                        "command": "image",
                        "input": args,
                        "result": result,
                        "timestamp": datetime.now().isoformat()
                    })
                
                elif command == "multimodal":
                    parts = args.split(maxsplit=1)
                    if len(parts) < 2:
                        print("❌ Please provide both text and image URL")
                        print("   Usage: multimodal <text> <image_url>")
                        continue
                    
                    text, image_url = parts
                    print("🔄 Analyzing multimodal input...")
                    result = await self.analyze_multimodal(text, image_url)
                    print(self.format_result(result))
                    
                    # Add to history
                    self.session_history.append({
                        "command": "multimodal",
                        "input": {"text": text, "image_url": image_url},
                        "result": result,
                        "timestamp": datetime.now().isoformat()
                    })
                
                elif command == "batch":
                    if not args:
                        print("❌ Please provide JSON file path")
                        continue
                    
                    await self.process_batch_file(args)
                
                elif command == "export":
                    if not args:
                        args = f"uniguru_session_{int(time.time())}.json"
                    
                    self.export_history(args)
                
                else:
                    print(f"❌ Unknown command: {command}")
                    print("💡 Type 'help' for available commands")
                
                # Show timing
                elapsed = (time.time() - start_time) * 1000
                if elapsed > 100:  # Only show if significant
                    print(f"⏱️  Command completed in {elapsed:.2f}ms")
                
                print()  # Add spacing
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye! Thanks for using Uniguru Sentiment Agent!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                print("💡 Type 'help' for available commands")

async def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Uniguru Sentiment Agent CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python uniguru_cli.py                           # Interactive mode
  python uniguru_cli.py --text "I love learning!" # Quick analysis
  python uniguru_cli.py --batch input.json        # Batch processing
  python uniguru_cli.py --persona kids --text "Fun!" # With persona
        """
    )
    
    parser.add_argument("--text", help="Text to analyze")
    parser.add_argument("--image", help="Image URL to analyze")
    parser.add_argument("--persona", choices=["youth", "kids", "spiritual"], 
                       default="youth", help="Analysis persona")
    parser.add_argument("--batch", help="JSON file for batch processing")
    parser.add_argument("--output", help="Output file for results")
    parser.add_argument("--interactive", action="store_true", 
                       help="Force interactive mode")
    
    args = parser.parse_args()
    
    cli = UniguruCLI()
    cli.current_persona = args.persona
    
    # Non-interactive modes
    if args.text or args.image or args.batch:
        if args.batch:
            await cli.process_batch_file(args.batch)
        else:
            # Single analysis
            if args.text and args.image:
                result = await cli.analyze_multimodal(args.text, args.image)
            elif args.text:
                result = await cli.analyze_text(args.text)
            elif args.image:
                result = await cli.analyze_image(args.image)
            
            print(cli.format_result(result))
            
            # Save output if requested
            if args.output:
                with open(args.output, 'w', encoding='utf-8') as f:
                    json.dump(result, f, indent=2, ensure_ascii=False)
                print(f"\n📄 Result saved to: {args.output}")
    else:
        # Interactive mode
        await cli.interactive_mode()

if __name__ == "__main__":
    asyncio.run(main())
