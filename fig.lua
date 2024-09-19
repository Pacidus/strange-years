if FORMAT:match "gfm" then
    function Image (elem)
        elem.attributes.style = "margin:auto; display: block;"
        return elem
    end
end
