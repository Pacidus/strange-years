if FORMAT:match "gfm" then
    function Figure (elem)
        elem.attributes.style = "margin:auto; display: block;"
        return elem
    end
end
