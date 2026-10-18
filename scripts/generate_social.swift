import AppKit
import Foundation
// macOS/AppKit shapes Arabic, Hebrew, Thai, Indic and CJK text using system fallbacks.
let root = URL(fileURLWithPath: CommandLine.arguments.count > 1 ? CommandLine.arguments[1] : FileManager.default.currentDirectoryPath)
let data = try Data(contentsOf: root.appendingPathComponent("content/locales.json"))
let locales = try JSONSerialization.jsonObject(with: data) as! [[String: Any]]
let cream = NSColor(calibratedRed: 0.96, green: 0.95, blue: 0.9, alpha: 1)
let gold = NSColor(calibratedRed: 0.92, green: 0.83, blue: 0.55, alpha: 1)
func text(_ str: String, _ rect: NSRect, size: CGFloat, color: NSColor, bold: Bool = false, rtl: Bool = false) {
    let para = NSMutableParagraphStyle()
    para.lineSpacing = 5
    para.baseWritingDirection = rtl ? .rightToLeft : .leftToRight
    para.alignment = rtl ? .right : .left
    var fontSize = size
    var attrs: [NSAttributedString.Key: Any] = [:]
    while true {
        attrs = [.font: NSFont.systemFont(ofSize: fontSize, weight: bold ? .bold : .regular), .foregroundColor: color, .paragraphStyle: para]
        let bounds = (str as NSString).boundingRect(with: NSSize(width: rect.width, height: 1000), options: [.usesLineFragmentOrigin, .usesFontLeading], attributes: attrs)
        if bounds.height <= rect.height || fontSize <= 18 { break }
        fontSize -= 1
    }
    (str as NSString).draw(with: rect, options: [.usesLineFragmentOrigin,.usesFontLeading], attributes: attrs)
}
for d in locales {
    let id = d["id"] as! String
    let bitmap = NSBitmapImageRep(bitmapDataPlanes:nil,pixelsWide:1200,pixelsHigh:630,bitsPerSample:8,samplesPerPixel:4,hasAlpha:true,isPlanar:false,colorSpaceName:.deviceRGB,bytesPerRow:0,bitsPerPixel:0)!
    NSGraphicsContext.saveGraphicsState()
    NSGraphicsContext.current = NSGraphicsContext(bitmapImageRep:bitmap)
    NSColor(calibratedRed:0.05,green:0.11,blue:0.09,alpha:1).setFill()
    NSRect(x:0,y:0,width:1200,height:630).fill()
    NSColor(calibratedRed:0.11,green:0.2,blue:0.12,alpha:1).setFill()
    NSBezierPath(ovalIn:NSRect(x:630,y:-120,width:720,height:900)).fill()
    if let icon = NSImage(contentsOf: root.appendingPathComponent("assets/apple-touch-icon.png")) {
        icon.draw(in:NSRect(x:65,y:501,width:60,height:60))
    }
    let rtl = ["ar","he"].contains(d["lang"] as! String)
    text(d["name"] as! String,NSRect(x:145,y:495,width:470,height:58),size:26,color:cream,bold:true,rtl:rtl)
    let hero = (d["hero"] as! [String])[0]
    text(hero,NSRect(x:65,y:225,width:610,height:230),size:60,color:gold,bold:true,rtl:rtl)
    text(d["seo"] as! String,NSRect(x:65,y:125,width:590,height:83),size:23,color:cream,rtl:rtl)
    text("App Store  ↗",NSRect(x:65,y:49,width:540,height:50),size:22,color:gold,bold:true)
    for (name,x,y,w) in [("1_nest_after",735.0,-45.0,220.0),("2_gameplay",940.0,100.0,220.0)] {
        if let screenshot=NSImage(contentsOf:root.appendingPathComponent("assets/screenshots/\(id)/\(name).webp")) {
            NSGraphicsContext.saveGraphicsState()
            let rect=NSRect(x:x,y:y,width:w,height:w*1564/720)
            let path=NSBezierPath(roundedRect:rect,xRadius:23,yRadius:23)
            path.addClip()
            screenshot.draw(in:rect)
            NSGraphicsContext.restoreGraphicsState()
            NSColor(calibratedWhite:1,alpha:0.2).setStroke();path.lineWidth=2;path.stroke()
        }
    }
    NSGraphicsContext.restoreGraphicsState()
    let jpeg=bitmap.representation(using:.jpeg,properties:[.compressionFactor:0.86])!
    try jpeg.write(to:root.appendingPathComponent("assets/og-\(id).jpg"))
}
print("Generated \(locales.count) localized social cards.")
