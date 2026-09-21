
$pClrs = @("White", "Red", "Black", "Yellow", "Violet")
$sClrs = @("Blue", "Orange", "Green", "Brown", "Slate")
$pairNumber = 1
$table = foreach ($major in $pClrs) {
    foreach ($minor in $sClrs) {
        [PSCustomObject]@{
            pNumber = $pairNumber
            pColor = $major
            sColor = $minor
        }
        $pairNumber++
    }
}

$table | Format-Table -AutoSize
