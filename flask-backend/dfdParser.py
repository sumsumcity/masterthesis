import json
import xml.etree.ElementTree as ET

# Component type definitions with their attributes and expected processing counts
componentTypes = [
    {"type": "trust boundary", "processingCount": 6, "detectionType": "attrib", "detectionKey": "style", "detectionValue": "group"},
    {"type": "bidirectional arrow", "processingCount": 7, "detectionType": "attrib", "detectionKey": "style", "detectionValue": "endArrow=classic;startArrow=classic"},
    {"type": "undirectional arrow", "processingCount": 7, "detectionType": "attrib", "detectionKey": "style", "detectionValue": "endArrow=classic"},
    {"type": "arrow", "processingCount": 2, "detectionType": "attrib", "detectionKey": "edge", "detectionValue": "1"},
    {"type": "adversary", "processingCount": 2, "detectionType": "attrib", "detectionKey": "style", "detectionValue": "shape=image;verticalLabelPosition=bottom;labelBackgroundColor=default;verticalAlign=top;aspect=fixed;imageAspect=0;image=data:image/svg+xml,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHhtbDpzcGFjZT0icHJlc2VydmUiIGlkPSJzdmcxIiB2ZXJzaW9uPSIxLjEiIHdpZHRoPSIyNCIgdmlld0JveD0iMCAtOTYwIDk2MCA5NjAiIGhlaWdodD0iMjQiPjxkZWZzIGlkPSJkZWZzMSIvPjxwYXRoIHN0eWxlPSJmaWxsOiM1NTAwMDAiIGlkPSJwYXRoMSIgZD0ibSA1OS4zMDksLTEzNi4xNTUgdiAtODguOTIxIGMgMCwtMTkuNjkyNjcgNS4xNTM2NjcsLTM3Ljc5NTMzIDE1LjQ2MSwtNTQuMzA4IDEwLjMwOCwtMTYuNTEyIDI0LjY5MjY2NywtMjkuMzgzNjcgNDMuMTU0LC0zOC42MTUgMzMuMjMwNjcsLTE2LjgyIDcwLjQxLC0zMC43MTczMyAxMTEuNTM4LC00MS42OTIgNDEuMTI4LC0xMC45NzQgODQuNDA5NjcsLTE2LjQ2MSAxMjkuODQ1LC0xNi40NjEgNDUuNDM2LDAgODguNzE4LDUuNDg3IDEyOS44NDYsMTYuNDYxIDQxLjEyOCwxMC45NzQ2NyA3OC4zMDczMywyNC44NzIgMTExLjUzOCw0MS42OTIgMTguNDYxMzMsOS4yMzEzMyAzMi44NDYsMjIuMTAzIDQzLjE1NCwzOC42MTUgMTAuMzA3MzMsMTYuNTEyNjcgMTUuNDYxLDM0LjYxNTMzIDE1LjQ2MSw1NC4zMDggdiA4OC45MjEgeiBtIDU5Ljk5OCwtNTkuOTk5IGggNDgwIHYgLTI4LjkyMiBjIDAsLTkuMTI4NjcgLTIuNDc0MzMsLTE2Ljk0OTMzIC03LjQyMywtMjMuNDYyIC00Ljk0ODY3LC02LjUxMjY3IC0xMS4xOTIzMywtMTEuODIwMzMgLTE4LjczMSwtMTUuOTIzIC0yNC41MTI2NywtMTIuNTEzMzMgLTU1LjYwMjMzLC0yNC4yNTcgLTkzLjI2OSwtMzUuMjMxIC0zNy42NjY2NywtMTAuOTc0NjcgLTc3Ljg1OSwtMTYuNDYyIC0xMjAuNTc3LC0xNi40NjIgLTQyLjcxNzMzLDAgLTgyLjkwOTMzLDUuNDg3MzMgLTEyMC41NzYsMTYuNDYyIC0zNy42NjY2NywxMC45NzQgLTY4Ljc1NjMzLDIyLjcxNzY3IC05My4yNjksMzUuMjMxIC03LjUzODY3LDQuMTAyNjcgLTEzLjc4MjMzLDkuNDEwMzMgLTE4LjczMSwxNS45MjMgLTQuOTQ5MzMsNi41MTI2NyAtNy40MjQsMTQuMzMzMzMgLTcuNDI0LDIzLjQ2MiB6IG0gMjQwLC0yNDQuNjE1IGMgLTM5LjEyNzMzLDAgLTcyLjI0MjMzLC0xMy41NTEzMyAtOTkuMzQ1LC00MC42NTQgLTI3LjEwMiwtMjcuMTAyIC00MC42NTMsLTYwLjk4NjMzIC00MC42NTMsLTEwMS42NTMgaCAtOS4yMzEgYyAtNS4yMzA2NywwIC05LjQ4NywtMS42NDEgLTEyLjc2OSwtNC45MjMgLTMuMjgyLC0zLjI4MiAtNC45MjMsLTcuNTM4MzMgLTQuOTIzLC0xMi43NjkgMCwtNS4yMzA2NyAxLjY0MSwtOS40ODcgNC45MjMsLTEyLjc2OSAzLjI4MiwtMy4yODIgNy41MzgzMywtNC45MjMgMTIuNzY5LC00LjkyMyBoIDkuMjMxIGMgMC41MTI2NywtMjUuMTI4IDYuMzA3MzMsLTQ3LjgzMjY3IDE3LjM4NCwtNjguMTE0IDExLjA3NjY3LC0yMC4yODIgMjYuODIsLTM3LjY3OTMzIDQ3LjIzLC01Mi4xOTIgdiAzOCBjIDAsNS4yMzA2NyAxLjY0MSw5LjQ4NyA0LjkyMywxMi43NjkgMy4yODIsMy4yODIgNy41MzgzMyw0LjkyMyAxMi43NjksNC45MjMgNS4yMzA2NywwIDkuNDg3LC0xLjY0MSAxMi43NjksLTQuOTIzIDMuMjgyLC0zLjI4MiA0LjkyMywtNy41MzgzMyA0LjkyMywtMTIuNzY5IHYgLTUzLjIzMSBjIDUuNzQ0LC0yIDEyLjAxMzMzLC0zLjYyODMzIDE4LjgwOCwtNC44ODUgNi43OTQ2NywtMS4yNTYgMTMuODU4NjcsLTEuODg0IDIxLjE5MiwtMS44ODQgNy4zMzMzMywwIDE0LjM5NzY3LDAuNjI4IDIxLjE5MywxLjg4NCA2Ljc5NDY3LDEuMjU2NjcgMTMuMDYzNjcsMi44ODUgMTguODA3LDQuODg1IHYgNTMuMjMxIGMgMCw1LjIzMDY3IDEuNjQxMzMsOS40ODcgNC45MjQsMTIuNzY5IDMuMjgyLDMuMjgyIDcuNTM4MzMsNC45MjMgMTIuNzY5LDQuOTIzIDUuMjMwNjcsMCA5LjQ4NywtMS42NDEgMTIuNzY5LC00LjkyMyAzLjI4MiwtMy4yODIgNC45MjMsLTcuNTM4MzMgNC45MjMsLTEyLjc2OSB2IC0zOCBjIDIwLjY2NiwxNC41MTI2NyAzNi40NzMzMywzMS45MSA0Ny40MjIsNTIuMTkyIDEwLjk0ODY3LDIwLjI4MTMzIDE2LjY3OTMzLDQyLjk4NiAxNy4xOTIsNjguMTE0IGggOS4yMzEgYyA1LjIzMDY3LDAgOS40ODcsMS42NDEgMTIuNzY5LDQuOTIzIDMuMjgyLDMuMjgyIDQuOTIzLDcuNTM4MzMgNC45MjMsMTIuNzY5IDAsNS4yMzA2NyAtMS42NDEsOS40ODcgLTQuOTIzLDEyLjc2OSAtMy4yODIsMy4yODIgLTcuNTM4MzMsNC45MjMgLTEyLjc2OSw0LjkyMyBoIC05LjIzMSBjIDAsNDAuNjY2NjcgLTEzLjU1MSw3NC41NTEgLTQwLjY1MywxMDEuNjUzIC0yNy4xMDI2NywyNy4xMDI2NyAtNjAuMjE4LDQwLjY1NCAtOTkuMzQ2LDQwLjY1NCB6IG0gMCwtNTkuOTk5IGMgMjIuNTEzMzMsMCA0MS40NzUsLTcuNzA1IDU2Ljg4NSwtMjMuMTE1IDE1LjQxLC0xNS40MTA2NyAyMy4xMTUsLTM0LjM3MjMzIDIzLjExNSwtNTYuODg1IGggLTE2MCBjIDAsMjIuNTEyNjcgNy43MDUzMyw0MS40NzQzMyAyMy4xMTYsNTYuODg1IDE1LjQxLDE1LjQxIDM0LjM3MTMzLDIzLjExNSA1Ni44ODQsMjMuMTE1IHoiLz48cGF0aCBzdHlsZT0ic3Ryb2tlLXdpZHRoOjAuNDIxNDUxO2ZpbGw6IzU1MDAwMCIgaWQ9InBhdGgxLTUzIiBkPSJtIDYzMy42MjM1NywtMzQwLjA2MTU1IC04My42NDE2NCwtODMuNjQxNjQgdiAtMTE5LjMwMjc1IGwgODMuNjQxNjQsLTgzLjY0MTY0IGggMTE5LjMwMjc1IGwgODMuNjQxNjQsODMuNjQxNjQgdiAxMTkuMzAyNzUgbCAtODMuNjQxNjQsODMuNjQxNjQgeiBtIDExLjYwNTkzLC03Ny40ODIxMyA0OC4wNDU0NSwtNDguMDQ1NDUgNDguMDQ1NDQsNDguMDQ1NDUgMTcuNzY1NDQsLTE3Ljc2NTQ0IC00OC4wNDU0NSwtNDguMDQ1NDQgNDguMDQ1NDUsLTQ4LjA0NTQ1IC0xNy43NjU0NCwtMTcuNzY1NDQgLTQ4LjA0NTQ0LDQ4LjA0NTQ1IC00OC4wNDU0NSwtNDguMDQ1NDUgLTE3Ljc2NTQ0LDE3Ljc2NTQ0IDQ4LjA0NTQ1LDQ4LjA0NTQ1IC00OC4wNDU0NSw0OC4wNDU0NCB6IG0gLTAuODQyOSw1Mi4xOTU0NyBoIDk3Ljc3NjY5IGwgNjkuMTE4MDEsLTY5LjExODAxIHYgLTk3Ljc3NjY5IGwgLTY5LjExODAxLC02OS4xMTgwMSBIIDY0NC4zODY2IGwgLTY5LjExODAxLDY5LjExODAxIHYgOTcuNzc2NjkgeiBtIDQ4Ljg4ODM1LC0xMTguMDA2MzUgeiIvPjwvc3ZnPg==;"},
    {"type": "note", "processingCount": 2, "detectionType": "attrib", "detectionKey": "style", "detectionValue": "text"},
    {"type": "asset", "processingCount": 3, "detectionType": "tag", "detectionValue": "object"},
]

# Input: XML body from threatFinderAI DFD
# Output: List of all Components in the DFD
def threatFinderAiDfdToComponentList(xml_string):
    root = ET.fromstring(xml_string)

    # Initialize variables for parsing components
    components = []  # List to store all parsed components
    currentComponent = {}  # Keeps track of the currently processed component
    procCount = 0  # Counter to track the number of processed elements for the current component

    # Iterate over XML elements
    for elem in root.iter():
        if not currentComponent: # If no component is currently being processed
            # Attempt to match the element to a component type
            for t in componentTypes:
                if t["detectionType"] == "tag" and elem.tag == t["detectionValue"]:
                    currentComponent = t
                    data = elem.attrib.copy()  # Copy element attributes to avoid mutability issues
                    data.update({"type": t["type"]})
                    procCount += 1  # Increment processing count
                    break  # Exit loop after matching
                elif t["detectionType"] == "attrib" and t["detectionKey"] in elem.attrib:
                    if t["detectionValue"] in elem.attrib[t["detectionKey"]]:
                        currentComponent = t
                        data = elem.attrib.copy()  # Copy element attributes to avoid mutability issues
                        data.update({"type": t["type"]})
                        procCount += 1  # Increment processing count
                        break  # Exit loop after matching
        elif procCount == currentComponent["processingCount"] - 1: # If currently processing a component - finalize the current component and reset for the next one
            data.update({k: v for k, v in elem.attrib.items() if k != "id" or k not in data or not data[k]})
            components.append(data) # Update data, exclude 'id' if it already has a value in 'data'
            currentComponent = {}
            procCount = 0
        else: # Continue processing the current component
            data.update({k: v for k, v in elem.attrib.items() if k != "id" or k not in data or not data[k]}) # Update data, exclude 'id' if it already has a value in 'data'
            procCount += 1

    return components

def componentToText(components):
    result = ""
    tbList = [] 

    # Get all trust boundaries
    for component in components:
        if component["type"] == "trust boundary":
            tb = {"id": component["id"], "value": component["value"], "x": component["x"], "y": component["y"], "width": component["width"], "height": component["height"]}
            tbList.append(tb)
    tbValues = [tb["value"] for tb in tbList]
    tbString = f"The system consists of {len(tbList)} trust boundaries called: {', '.join(tbValues)}. "
    result = result + tbString

    # Now textulize the rest and check always if it is in a trustBoundary
    for component in components:
        if component["type"] == "asset":
            tbFound=False
            assetStr = f"There is an asset {component['assetname']} called {component['label']}"
            for tb in tbList:
                if component["parent"] == tb["id"]:
                    assetStr = assetStr + f" which is in the trust boundary {tb['value']}"
                    tbFound = True
                    break
            if not tbFound:
                if float(component["x"]) >= float(tb["x"]) and float(component["x"]) <= (float(tb["x"]) + float(tb["width"])):
                    if float(component["y"]) >= float(tb["y"]) and float(component["y"]) <= (float(tb["y"]) + float(tb["height"])):
                        assetStr = assetStr + f" which is in the trust boundary {tb['value']}"
                        break
            assetStr = assetStr + ". "
            result = result + assetStr
        elif component["type"] == "arrow":
            sourceAsset = findById(components, component["source"])
            targetAsset = findById(components, component["target"])
            if sourceAsset is not None and targetAsset is not None:
                sourceLabel = sourceAsset.get("label", sourceAsset.get("type", "Unknown"))
                targetLabel = targetAsset.get("label", targetAsset.get("type", "Unknown"))
                arrowStr = f"The asset {sourceLabel} points to asset {targetLabel} with an arrow. "
                result = result + arrowStr
        elif component["type"] == "bidirectional arrow":
            sourceAsset = findById(components, component["source"])
            targetAsset = findById(components, component["target"])
            if sourceAsset is not None and targetAsset is not None:
                sourceLabel = sourceAsset.get("label", sourceAsset.get("type", "Unknown"))
                targetLabel = targetAsset.get("label", targetAsset.get("type", "Unknown"))
                arrowStr = f"The asset {sourceLabel} points to asset {targetLabel} with a bidirectional arrow ({component['value']}). "
                result = result + arrowStr
        elif component["type"] == "undirectional arrow":
            sourceAsset = findById(components, component["source"])
            targetAsset = findById(components, component["target"])
            if sourceAsset is not None and targetAsset is not None:
                sourceLabel = sourceAsset.get("label", sourceAsset.get("type", "Unknown"))
                targetLabel = targetAsset.get("label", targetAsset.get("type", "Unknown"))
                arrowStr = f"The asset {sourceLabel} points to asset {targetLabel} with an undirectional arrow ({component['value']}). "
                result = result + arrowStr
        elif component["type"] == "adversary":
            assetStr = f"There is an adversary in the drawing"
            for tb in tbList:
                if component["parent"] == tb["id"]:
                    assetStr = assetStr + f" which is in the trust boundary {tb['value']}"
            assetStr = assetStr + ". "
            result = result + assetStr
        elif component["type"] == "note":
            noteStr = f"There is an note in the drawing which says: {component['value']}. "
            for tb in tbList:
                if component["parent"] == tb["id"]:
                    noteStr = noteStr + f"The note is in the trust boundary {tb['value']}. "
            result = result + noteStr
    
    print("System description is: " + result)
    return result
        

# Find item in a list of dicts by id
def findById(items, target_id):
    for item in items:
        if item.get("id") == target_id:
            return item
    return None  # Return None if no match is found
