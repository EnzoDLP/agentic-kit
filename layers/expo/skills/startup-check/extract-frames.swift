// Extracts frames from a simulator recording so each one can be inspected as an image.
// Usage: swift extract-frames.swift <video.mov> <out-dir> [interval-seconds=0.05] [max-width=480]
// Writes <out-dir>/frame-<ms>.jpg for every frame that differs from the previous kept one,
// and <out-dir>/frames.tsv (ms, file, mean luminance 0-255, changed pixels %).

import AVFoundation
import CoreGraphics
import Foundation
import ImageIO
import UniformTypeIdentifiers

let args = CommandLine.arguments
guard args.count >= 3 else {
  FileHandle.standardError.write(
    "usage: swift extract-frames.swift <video> <out-dir> [interval=0.05] [max-width=480]\n"
      .data(using: .utf8)!)
  exit(1)
}

let videoURL = URL(fileURLWithPath: args[1])
let outDir = URL(fileURLWithPath: args[2], isDirectory: true)
let interval = args.count > 3 ? Double(args[3]) ?? 0.05 : 0.05
let maxWidth = args.count > 4 ? Int(args[4]) ?? 480 : 480
// A frame is kept when more than this share of its sampled pixels changed.
let changeThreshold = 0.5

try FileManager.default.createDirectory(at: outDir, withIntermediateDirectories: true)

let asset = AVURLAsset(url: videoURL)
let generator = AVAssetImageGenerator(asset: asset)
generator.appliesPreferredTrackTransform = true
generator.requestedTimeToleranceBefore = .zero
generator.requestedTimeToleranceAfter = .zero
generator.maximumSize = CGSize(width: maxWidth, height: maxWidth * 3)

let duration = CMTimeGetSeconds(asset.duration)
let sampleSide = 32

func sample(_ image: CGImage) -> [UInt8] {
  var pixels = [UInt8](repeating: 0, count: sampleSide * sampleSide)
  let context = CGContext(
    data: &pixels, width: sampleSide, height: sampleSide, bitsPerComponent: 8,
    bytesPerRow: sampleSide, space: CGColorSpaceCreateDeviceGray(),
    bitmapInfo: CGImageAlphaInfo.none.rawValue)!
  context.draw(image, in: CGRect(x: 0, y: 0, width: sampleSide, height: sampleSide))
  return pixels
}

func writeJPEG(_ image: CGImage, to url: URL) {
  let destination = CGImageDestinationCreateWithURL(
    url as CFURL, UTType.jpeg.identifier as CFString, 1, nil)!
  CGImageDestinationAddImage(
    destination, image, [kCGImageDestinationLossyCompressionQuality: 0.7] as CFDictionary)
  CGImageDestinationFinalize(destination)
}

var previous: [UInt8]? = nil
var rows = ["ms\tfile\tluminance\tchanged_pct"]
var time = 0.0
var kept = 0

while time <= duration {
  let cmTime = CMTime(seconds: time, preferredTimescale: 600)
  if let image = try? generator.copyCGImage(at: cmTime, actualTime: nil) {
    let pixels = sample(image)
    let luminance = Double(pixels.reduce(0) { $0 + Int($1) }) / Double(pixels.count)
    var changedPct = 100.0
    if let previous {
      let changed = zip(pixels, previous).filter { abs(Int($0) - Int($1)) > 6 }.count
      changedPct = Double(changed) * 100 / Double(pixels.count)
    }
    let ms = Int((time * 1000).rounded())
    if previous == nil || changedPct > changeThreshold {
      let name = String(format: "frame-%06d.jpg", ms)
      writeJPEG(image, to: outDir.appendingPathComponent(name))
      rows.append("\(ms)\t\(name)\t\(String(format: "%.0f", luminance))\t\(String(format: "%.1f", changedPct))")
      previous = pixels
      kept += 1
    }
  }
  time += interval
}

try rows.joined(separator: "\n").write(
  to: outDir.appendingPathComponent("frames.tsv"), atomically: true, encoding: .utf8)
print("duration \(String(format: "%.2f", duration)) s, \(kept) distinct frames → \(outDir.path)")
