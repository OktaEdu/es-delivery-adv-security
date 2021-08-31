#/bin/bash
dir=`readlink -f $BASH_SOURCE`
dir=`echo "$dir" | sed -e "s/\/set_path.sh//"`
echo "Adding to path: $dir"
export PATH=$PATH:$dir
